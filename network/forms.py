from django import forms
from .models import Post, PostComment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'image', 'body'
            ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = [
            'comment_body'
        ]