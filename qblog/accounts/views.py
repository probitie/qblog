from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

REGISTRATION_TEMPLATES_PATH = "registration/"


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):

    template_name = f'{REGISTRATION_TEMPLATES_PATH}password_reset.html'
    email_template_name = f'{REGISTRATION_TEMPLATES_PATH}password_reset_email.html'
    # subject_template_name = 'accounts:password_reset_subject'  # does not exists
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('accounts:password_reset_done')

