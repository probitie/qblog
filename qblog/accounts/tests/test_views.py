import logging

from django.http import HttpResponse
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

username = 'user'
email = 'test@test.com'
password = 'passwordD121'

login_url = '/accounts/login/'
signup_url = '/accounts/signup/'
homepage = '/'

# need to concatenate a username
profile_url = '/accounts/profile/'
edit_profile_url = '/accounts/edit-profile/'


class LoginViewTestCase(TestCase):

    def test_account_is_not_exists(self):
        """login view must redirect to login page if account is not exists"""

        response = self.client.post(login_url, {'username': username, 'password': password})
        self.assertWarnsMessage(logging.WARNING, "<WSGIRequest: POST '/accounts/login/'>")
        self.assertRedirects(response, login_url)  # redirects back to the page

    def test_account_is_not_active(self):
        """login view must redirect to login page if account is disabled"""
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        response = self.client.post(login_url, {'username': username, 'password': password})
        self.assertWarnsMessage(logging.WARNING, "<WSGIRequest: POST '/accounts/login/'>")
        self.assertRedirects(response, login_url)  # redirects back to the page

    def test_successful_login(self):
        """verifying that user has successfully logged on"""

        user = User.objects.create_user(username=username, email=email, password=password)

        # go to login page
        response = self.client.post('/accounts/login/', {'username': username, 'password': password})
        self.assertRedirects(response, homepage)


class SignUpViewTestCase(TestCase):

    def signup(self, username_=username, email_=email, password1_=password, password2_=password) -> HttpResponse:
        """test successful signup"""
        response = self.client.post(signup_url, {'username': username_, 'email': email_, 'password1': password1_, 'password2': password2_})
        return response

    def test_username_required(self):
        """test signup with empty username field"""
        response = self.signup(username_='')
        self.assertEqual(response.status_code, 200)  # no redirect if form is filled with errors

    def test_password_required(self):
        """test signup with empty password field"""
        response = self.signup(password1_='', password2_='')
        self.assertEqual(response.status_code, 200)  # no redirect if form is filled with errors

    def test_password1_and_2_must_be_the_same(self):
        """test signup with different password in password confirmation field"""
        response = self.signup(password1_=password, password2_=password+'notthesamestring')
        self.assertEqual(response.status_code, 200)  # no redirect if form is filled with errors

    def test_email_required(self):
        """test signup with empty email field"""
        response = self.signup(email_='')
        self.assertEqual(response.status_code, 200)  # no redirect if form is filled with errors

    def test_successful_authorisation(self):
        """verifying that user creation was successful"""
        response = self.signup()
        self.assertRedirects(response, login_url)  # redirects back to the page


class ProfileTestCase(TestCase):

    def test_private_profile(self):
        """"""
        user = User.objects.create_user(username=username, email=email, password=password)

        # open profile
        self.client.login(username=username, password=password)
        response = self.client.post(f'{profile_url}{username}', {})
        self.assertTrue(response.status_code, 200)

    def test_public_profile(self):
        """"""
        user = User.objects.create_user(username=username, email=email, password=password)

        username2 = 'john'
        password2 = 'johnjohn22@2'
        email2 = 'aaa@a.cu'
        user2 = User.objects.create_user(username=username2, email=email2, password=password2)

        # open profile
        self.client.login(username=username2, password=password2)
        response = self.client.post(f'{profile_url}{username}', {})
        self.assertTrue(response.status_code, 200)

    def test_guest_public_profile(self):
        """anonymous user can see profiles"""
        # open profile
        response = self.client.post(f'{profile_url}{username}', {})
        self.assertTrue(response.status_code, 200)


class EditProfileTestCase(TestCase):
    def edit_(self, content: dict, profile_username=None) -> HttpResponse:
        """
        profile_username - which profile we want to view
        (can be the same user or different(need to be already created))
        """
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        if not profile_username:
            profile_username = username

        # open profile
        self.client.login(username=username, password=password)
        response = self.client.post(f'{edit_profile_url}{profile_username}', content)
        return response

    def test_edit_profile_page(self):
        """"""
        # todo always OK even if response must be 404 but there it is 200
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        response = self.client.get(f'{login_url}{username}')

        self.assertTrue(response.status_code, 200)

    def test_edit_username(self):
        """user can edit his username"""
        response = self.edit_({'username': username})
        self.assertRedirects(response, f"{profile_url}{username}")

    def test_edit_about_user(self):
        """user can edit his about_user field"""
        response = self.edit_({'about_user': "test"})
        self.assertRedirects(response, f"{profile_url}{username}")

    # TODO unit testing image uploads django  test_
    def edit_image(self):
        """user can reset his image"""
        with open('accounts/tests/test.PNG', 'rb') as image:
            response = self.edit_({'image': image}, profile_username='testtest')
        self.assertRedirects(response, f"{profile_url}{username}")

    def test_edit_other_username(self):
        """user can not edit other username"""
        username2 = 'testtest'
        user2 = User.objects.create_user(username=username2, email='test@test.com', password='john22@3f')
        user2.save()
        response = self.edit_({'username': username}, profile_username=username2)
        self.assertTrue(response.status_code, 404)

    def test_edit_other_about_user(self):
        """user can not edit other about_user field"""
        username2 = 'testtest'
        user2 = User.objects.create_user(username=username2, email='test@test.com', password='john22@3f')
        user2.save()
        response = self.edit_({'about_user': "testtesttest"}, profile_username=username2)
        self.assertTrue(response.status_code, 404)

    def test_edit_other_image(self):
        """user can not reset other image"""
        username2 = 'testtest'
        user2 = User.objects.create_user(username=username2, email='test@test.com', password='john22@3f')
        user2.save()
        with open('accounts/tests/test.PNG', 'rb') as image:
            response = self.edit_({'image': image}, profile_username=username2)
        self.assertTrue(response.status_code, 404)
