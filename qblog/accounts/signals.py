from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """creates user profile object automatically when user object is saving to db"""
    if created:
        Profile.objects.create(user=instance)
