from django import forms
from django.conf import settings

from .models import Post

POST_MIN_LEN = getattr(settings, "POST_MIN_LEN", None)


class PostForm(forms.ModelForm):
    """Форма добавления поста."""

    class Meta:
        model = Post
        fields = ("text", "group")
