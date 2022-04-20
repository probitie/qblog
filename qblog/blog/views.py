import logging

from django.views import generic
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse

from .models import Post, CommentModel
from .forms import SearchPostForm, CommentForm

# Create your views here.
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t %(asctime)s.%(msecs)03d:%(filename)s:%(lineno)d:%(message)s',
                            datefmt='%H:%M:%S')

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

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data["your_name"]
            content = form.cleaned_data["comment_text"]
            comment = CommentModel(your_name=author, comment_text=content)
            comment.save()
            return redirect(reverse(f"blog:post_detail/"))

    post = get_object_or_404(Post, slug=slug)
    comments = CommentModel.objects.filter(post=post)
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


def search_post_form(request: HttpRequest):
    """"""

    if request.method == 'POST':
        form = SearchPostForm(request.POST)
        logging.debug("method is post, processing data")
        if form.is_valid():
            post_title = form.cleaned_data['post_title']
            try:
                post = Post.objects.get(title=post_title)
            except post_title.DoesNotExist():
                raise Http404('This post does not exist')

            return HttpResponseRedirect(f'/{post.slug}')
    else:
        logging.debug("method is get, showing empty form")
        form = SearchPostForm()
        context = {
            'form': form,
        }
    return render(request, 'blog/search_post.html', context)
