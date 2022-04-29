from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from blog.models import STATUS

User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EditProfileForm(forms.Form):
    username = forms.CharField(required=False)
    about_user = forms.CharField(required=False)
    image = forms.ImageField(required=False)

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
                raise forms.ValidationError(
                    'A user with that username already exists.')
        return username
