from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    pass

# it will be created with new user instance - discrete model because user may customise it
class Profile(models.Model):

    about_user = models.TextField()
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# for custom user model (I`ve got some errors so left it for the next time)
'''class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.admin = is_admin
        user.active = is_active
        user.staff = is_staff
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

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.admin = is_admin
        user.active = is_active
        user.staff = is_staff
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    username = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name='Username')
    email = models.EmailField('email address', unique=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    class Meta:
        pass'''

# Create your models here.
