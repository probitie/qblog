import logging

from django import forms
from .models import STATUS, Post


class SearchPostForm(forms.Form):
    post_title = forms.CharField(label="post_title", max_length=100)


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class AddPostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS)

    def assert_slug_not_exists(self, slug) -> None:
        """

        :raises forms.ValidationError
        """
        if Post.objects.filter(slug=slug):
            logging.debug(f"slug {slug} exists")
            raise forms.ValidationError("This title already exists")
        else:
            logging.debug(f"slug {slug} not exists")
