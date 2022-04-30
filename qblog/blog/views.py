import logging

from django.views import generic
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required

from qblog import settings
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .forms import SearchPostForm, CommentForm, AddPostForm

# Create your views here.
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t %(asctime)s.%(msecs)03d:%(filename)s:%(lineno)d:%(message)s',
                            datefmt='%H:%M:%S')


User = get_user_model()

class PostList(generic.ListView):
    """
    Return all posts that are with status 1 (published) and order from the latest one.
    """
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'


def _increment_views_count(obj: Post):
    """increments views_count field (need to use for each session once)"""
    logging.debug("increment view count")
    obj.views_count += 1
    obj.save()


def _increment_views_count_for_session(request: HttpRequest, obj: Post) -> int:
    """
    anonymous user views counter

    checks "views" field in session and when obj.slug not presents in session
     increments count if not viewed for this session
     and add obj.slug to session
    obj: where we want to increment count
    returns: views count
    """
    if not request.session.get("viewed_pages", False):
        logging.debug("first view of the post for this session")

        try:
            request.session["viewed_pages"]
        except KeyError:
            request.session["viewed_pages"] = []

        request.session["viewed_pages"] += obj.slug
        _increment_views_count(obj)
    else:
        logging.debug("post already viewed")

    return obj.views_count


def post_detail(request: HttpRequest, slug):
    POST_DETAIL_PATH = f"/{slug}/"

    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        if not request.user.is_authenticated:
            logging.debug(f"User must be authenticated to write comments")
            return redirect(reverse(f'accounts:login'))

        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            text = form.cleaned_data["text"]
            comment = Comment(author=author, text=text, post=post)
            comment.save()
            return redirect(POST_DETAIL_PATH)

    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    # Number of visits to this view, as counted in the session variable.
    views_count = _increment_views_count_for_session(request, post)

    context = {
        "object": post,
        "views_count": views_count,
        "comments": comments,
        "form": form
    }

    return render(request, 'blog/post_detail.html', context=context)

@login_required
def add_post(request):
    logging.debug(f"1")
    if request.method == "POST":
        logging.debug(f"2")
        form = AddPostForm(request.POST)
        logging.debug(f"3")
        if form.is_valid():
            logging.debug(f"4")
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            status = form.cleaned_data["status"]
            logging.debug(f"5")
            slug = Post.get_slug_from_title(title)
            logging.debug(f"6")
            # form.assert_slug_not_exists(slug)  # TODO connect checking if the slug is already exists
            author = User.objects.get(id=request.user.id)
            logging.debug(f"7")
            logging.debug(f"slug is {slug}")
            post = Post(
                        title=title,
                        slug=slug,
                        author=author,
                        content=content,
                        status=status,
                        )
            logging.debug(f"8")
            post.save()
            logging.debug(f"9")
            return redirect("accounts:profile", username=author.username)
    else:
        logging.debug(f"10")
        form = AddPostForm()
    logging.debug(f"11")
    return render(request, f"blog/add_post.html", {'form': form})

@login_required
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.user == post.author:
        logging.debug(f"deleting post {slug=}")
        Post.objects.get(slug=slug).delete()
    else:
        logging.debug(f"user {request.user} can not delete posts of another user ({post.author})")
    return redirect(f"accounts:profile", username=request.user.username)


@login_required
def publish_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.user == post.author:
        logging.debug(f"publishing post {slug=}")
        post.publish()
        post.save()
    else:
        logging.debug(f"user {request.user} can not publish posts of another user ({post.author})")
    return redirect(f"accounts:profile", username=request.user.username)


def search_post_form(request: HttpRequest):
    """"""

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

