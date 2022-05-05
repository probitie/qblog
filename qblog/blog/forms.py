from django import forms
from .models import STATUS


class SearchPostForm(forms.Form):
    post_title = forms.CharField(label="post_title", max_length=100)


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class AddPostForm(forms.Form):
    title = forms.CharField()
    image = forms.ImageField(required=False)
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS)
