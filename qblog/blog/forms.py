from django import forms


class SearchPostForm(forms.Form):
    post_title = forms.CharField(label="post_title", max_length=100)


class CommentForm(forms.Form):
    your_name = forms.CharField(max_length=20)
    comment_text = forms.CharField(widget=forms.Textarea)

