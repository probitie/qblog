from django.test import TestCase

class LoginViewTestCase(TestCase):

    def test_account_is_not_exists(self):
        """login view must redirect to login page if account is not exists"""
