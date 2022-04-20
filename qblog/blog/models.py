from django.db import models
from django.contrib.auth.models import User
from qblog import settings

# Create your models here.
STATUS_DRAFT = 0
STATUS_PUBLISHED = 1
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)  # path to post in url
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    views_count = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    your_name = models.CharField(max_length=20)
    comment_text = models.TextField(max_length=500)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by Name: {self.your_name}"
