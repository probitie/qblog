from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import CustomUser, Profile

User = get_user_model()

username = 'user'
email = 'test@test.com'
password = 'passwordD121'

class UserTestCase(TestCase):

    def test_create_user(self):
        """"""
        '''user = CustomUser.objects.create(username=)
        self.assertEquals(str(product), 'ToyCar')
        print("IsInstance : ",isinstance(product,Product))
        self.assertTrue(isinstance(product,Product))'''

    def test_create_staffuser(self):
        """"""

    def test_create_superuser(self):
        """"""

class ProfileTestCase(TestCase):

    def test_profile_model(self):
        """"""
        # todo just fill all fields
