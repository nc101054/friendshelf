from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["kind", "title", "thoughts", "is_public"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {"content": forms.TextInput(attrs={"placeholder": "说点什么…"})}