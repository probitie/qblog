import os
import logging

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from . import forms
from .models import Profile, User
from blog.models import Post
from qblog import settings
from qblog.shortcuts import get_or_none
REGISTRATION_TEMPLATES_PATH = "registration/"


def signup(request):

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        logging.debug("posting info to signup page")
        if form.is_valid():
            logging.debug("the form is valid, saving")
            form.save()
            return redirect(f'accounts:login')
        else:
            logging.debug("the form is NOT valid")
            return redirect(f'accounts:signup')  # TODO provide an error message

    else:
        logging.debug("getting signup page")
        form = forms.SignUpForm()
        template = 'registration/signup.html'
        context = {'form': form}
        return render(request, template, context)

def profile(request, username):
    """to render public or private is controls by is_current_user"""

    current_user = get_or_none(User, id=request.user.id)
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, pk=profile_user.id)
    post_list = Post.objects.filter(author=profile_user.id)

    is_current_user = current_user == profile_user
    logging.debug(f"showing {profile_user} {'private' if is_current_user else 'public'} profile to {current_user}")

    return render(request, "registration/profile/profile.html",
                  context={"user": profile_user,
                           "is_current_user": is_current_user,
                           "profile": profile,
                           "user_post_list": post_list})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = forms.EditProfileForm(request.user.username, request.POST, request.FILES)
        if form.is_valid():
            about_user = form.cleaned_data["about_user"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            if username:
                user.username = username
            user.save()
            if about_user:
                profile.about_user = about_user
            if image:
                profile.image = image
            profile.save()
            return redirect("accounts:profile", username=user.username)
    else:
        form = forms.EditProfileForm(request.user.username)
    return render(request, f"{REGISTRATION_TEMPLATES_PATH}/profile/edit_profile.html", {'form': form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):

    template_name = f'{REGISTRATION_TEMPLATES_PATH}password_reset.html'
    email_template_name = f'{REGISTRATION_TEMPLATES_PATH}password_reset_email.html'
    # subject_template_name = 'accounts:password_reset_subject'  # does not exists
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('accounts:password_reset_done')

