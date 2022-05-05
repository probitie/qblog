import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Post, Comment, STATUS_PUBLISHED
from .forms import SearchPostForm, CommentForm, AddPostForm

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t %(asctime)s.%(msecs)03d:%(filename)s:%(lineno)d:%(message)s',
                            datefmt='%H:%M:%S')

User = get_user_model()  # because I use custom model


class PostList(generic.ListView):
    """Return all posts that are with status 1 (published) and order from the latest one."""
    queryset = Post.objects.filter(status=STATUS_PUBLISHED).order_by('-created_at')
    template_name = 'blog/index.html'


def _get_views_count(post: Post) -> int:
    """returns the number of views of the specified post"""
    return len(post.viewed_by.all())


def _register_user_view(request: HttpRequest, post: Post) -> None:
    """add user from request to Post.viewed_by field"""

    # if the user is authenticated not already viewed the post
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        if not post.viewed_by.filter(pk=user.id).exists():
            post.viewed_by.add(user)
            post.save()


def _handle_comments(request: HttpRequest, post: Post, post_slug: str) -> HttpResponseRedirect:
    """
    handle comments on page

    :raises Http404 if request method is not POST
    """

    # todo add to comment form button that will mark it as comment form and then handle it here
    if request.method == "POST":
        if not request.user.is_authenticated:
            logging.debug(f"CustomUser must be authenticated to write comments")
            return redirect(f'accounts:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            text = form.cleaned_data["text"]
            comment = Comment(author=author, text=text, post=post)
            comment.save()
            return redirect(reverse_lazy("blog:post_detail"), slug=post_slug)
    raise Http404("no comments have been posted, nothing to handle")


def post_detail(request: HttpRequest, slug) -> HttpResponse:
    """
    detail view of the post

    I use function instead of a class, but it could be rewritten to a class at any time
    """

    post = get_object_or_404(Post, slug=slug)

    # easier to ask for forgiveness than permission ))
    try:
        return _handle_comments(request, post, slug)
    except Http404:
        pass  # nothing to handle

    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    _register_user_view(request, post)
    views_count = _get_views_count(post)

    context = {
        "object": post,
        "views_count": views_count,
        "comments": comments,
        "form": form
    }

    return render(request, 'blog/post_detail.html', context=context)


@login_required
def add_post(request: HttpRequest) -> HttpResponse:
    """view for adding post"""
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]
            slug = Post.get_slug_from_title(title)
            author = User.objects.get(id=request.user.id)

            post = Post(
                        title=title,
                        slug=slug,
                        author=author,
                        image=image,
                        content=content,
                        status=status,
                        )
            post.save()
            # redirect to a profile because it is using only there
            return redirect("accounts:profile", username=author.username)
    else:
        form = AddPostForm()
    return render(request, f"blog/add_post.html", {'form': form})


@login_required
def delete_post(request, slug) -> HttpResponseRedirect:
    """
    view for deleting post

    only an owner is able to delete the post
    """
    post = Post.objects.get(slug=slug)
    if request.user == post.author:
        Post.objects.get(slug=slug).delete()
    else:
        logging.debug(f"user {request.user} can not delete posts of another user ({post.author})")
    return redirect(f"accounts:profile", username=request.user.username)


@login_required
def publish_post(request, slug):
    """
    view for publishing post (make it visible to other users and from main page)

    only an owner is able to publish the post
    """
    post = Post.objects.get(slug=slug)
    if request.user == post.author:
        post.publish()
        post.save()
    else:
        logging.debug(f"user {request.user} can not publish posts of another user ({post.author})")

    return redirect(f"accounts:profile", username=request.user.username)


def search_post(request: HttpRequest):
    """a view for finding posts by symbols their titles contain"""

    if request.method == 'POST':
        form = SearchPostForm(request.POST)
        if form.is_valid():
            post_title = form.cleaned_data['post_title']
            post_list = Post.objects.filter(title__contains=post_title)
            context = {
                "form": form,
                "post_list": post_list
            }

            return render(request, f'blog/search_post.html', context=context)
    else:
        form = SearchPostForm()
        context = {
            'form': form,
            "post_list": []
        }
    return render(request, 'blog/search_post.html', context)
