from django import forms
from django.conf import settings

from .models import Post


class PostForm(forms.ModelForm):
    """Форма добавления поста."""

    class Meta:
        model = Post
        fields = ("text", "group")
