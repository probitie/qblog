import logging

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib.auth import authenticate, login

from . import forms
from .models import Profile, CustomUser
from blog.models import Post
from qblog.shortcuts import get_or_none

User = get_user_model()

def login_view(request):
    """A view for login a user"""
    template = 'registration/login.html'
    form = forms.LoginForm
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('blog:main')
            else:
                logging.warning(request, "Your account is disabled!")
                return redirect('accounts:login')
        else:
            logging.warning(request, "The username or password are not valid!")
            return redirect('accounts:login')
    else:
        context = {'form': form}
        return render(request, template, context)

# I can use class-based views as well as function views
class SignUpView(CreateView):
    """A view for create a new user"""
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "registration/signup.html"


def profile(request, username):
    """
    A view for showing user`s profile

    is_current_user variable in templates uses for showing public or private profile
    """

    current_user = get_or_none(CustomUser, id=request.user.id)
    profile_user = get_object_or_404(CustomUser, username=username)
    profile_obj = get_object_or_404(Profile, pk=profile_user.id)
    post_list = Post.objects.filter(author=profile_user.id)

    is_current_user = current_user == profile_user
    logging.debug(f"showing {profile_user} {'private' if is_current_user else 'public'} profile to {current_user}")

    return render(request, "registration/profile/profile.html",
                  context={"user": profile_user,
                           "is_current_user": is_current_user,
                           "profile": profile_obj,
                           "user_post_list": post_list})


@login_required
def edit_profile(request):
    """A view for editing user`s profile"""
    if request.method == "POST":
        form = forms.EditProfileForm(request.user.username, request.POST, request.FILES)
        if form.is_valid():
            about_user = form.cleaned_data["about_user"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]
            user = CustomUser.objects.get(id=request.user.id)
            profile_obj = Profile.objects.get(user=user)
            if username:
                user.username = username
            user.save()
            if about_user:
                profile_obj.about_user = about_user
            if image:
                profile_obj.image = image
            profile_obj.save()
            return redirect("accounts:profile", username=user.username)
    else:
        form = forms.EditProfileForm(request.user.username)
    return render(request, f"registration/profile/edit_profile.html", {'form': form})


def password_reset_request(request):
    """a view that handles password reset request"""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',  # todo use domain from settings in production
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect(reverse_lazy("accounts:password_reset_done"))
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
