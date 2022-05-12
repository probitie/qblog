from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from qblog.settings import USERDATA_URL

from qblog import model_file_cleaner
model_file_cleaner.setup()


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("User must have username")
        if not password:
            raise ValueError("User must have a password")
        if not email:
            raise ValueError("User must have a email")

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_admin = is_admin
        user.is_active = is_active
        user.is_staff = is_staff
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password,
            is_staff=True
            )
        return user

    def create_superuser(self, username, email, password=None, is_active=True, is_staff=True, is_admin=True):
        if not username:
            raise ValueError("User must have username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = is_admin
        user.email = email
        user.is_active = is_active
        user.is_staff = is_staff
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    objects = UserManager()
    # add additional fields in here

    def __str__(self):
        return self.username

def upload_icon_to(instance, filename):
    """generates path for storing user`s icon"""
    return f'{USERDATA_URL}{instance.user.id}/icons/{filename}'

# it will be created with new user instance - discrete model because user may customise it
class Profile(models.Model):

    about_user = models.TextField()
    image = models.ImageField(upload_to=upload_icon_to, null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
