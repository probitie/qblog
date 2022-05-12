from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import login_view, SignUpView, profile, edit_profile, password_reset_request
from django.contrib.auth import get_user_model

User = get_user_model()

username = 'user'
email = 'test@test.com'
password = 'passwordD121'

class UrlTest(TestCase):

    def test_LoginView(self):

        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func, login_view)

    def test_SignUpView(self):

        url = reverse('accounts:signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_ProfileView(self):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        url = reverse('accounts:profile', kwargs={'username': user.username})
        self.assertEquals(resolve(url).func, profile)

    def test_EditProfileView(self):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        url = reverse('accounts:edit_profile', kwargs={'username': user.username})
        self.assertEquals(resolve(url).func, edit_profile)
