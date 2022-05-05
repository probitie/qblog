from datetime import datetime
from django.db import models
from qblog import settings


STATUS_DRAFT = 0
STATUS_PUBLISHED = 1

# post status: Draft - visible only for author or Publish - visible for everyone
STATUS = (
    (STATUS_DRAFT, "Draft"),
    (STATUS_PUBLISHED, "Publish")
)

def upload_img_to(instance, filename):
    """generates path for storing post images"""
    # date string is used for making each file unique
    return f'userdata/{instance.author.id}/img/{datetime.now().strftime("%y%m%d%H%M%S%f")}__{filename}'

class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    image = models.ImageField(upload_to=upload_img_to, null=True, blank=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    viewed_by = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_draft(self) -> bool:
        """Checks if post is draft"""
        return self.status == STATUS_DRAFT

    def publish(self) -> None:
        """make post status PUBLISHED"""
        self.status = STATUS_PUBLISHED

    @staticmethod
    def get_slug_from_title(title: str) -> str:
        """makes slug from title"""
        return title.lower().replace(" ", "_").replace(',', '').replace('.', '').replace('%', '').replace('#', '').replace('@,', '').replace('&', '').replace('*', '').replace('(', '').replace(')', '').replace('$', '')


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"by: {self.author}"
