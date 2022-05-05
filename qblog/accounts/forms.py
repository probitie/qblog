from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms as django_forms
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class EditProfileForm(django_forms.Form):
    username = django_forms.CharField(required=False)
    about_user = django_forms.CharField(required=False)
    image = django_forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        """
        This function throws an exception if the username has already been
        taken by another user
        """

        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise django_forms.ValidationError(
                    'A user with that username already exists.')
        return username


class LoginForm(AuthenticationForm):
    username = django_forms.CharField(label="Username", required=True, max_length=30,
                                      widget=django_forms.TextInput(attrs={
                                          'class': 'form-control',
                                          'name': 'username'}))
    password = django_forms.CharField(label="Password", required=True, max_length=30,
                                      widget=django_forms.PasswordInput(attrs={
                                          'class': 'form-control',
                                          'name': 'password'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")
