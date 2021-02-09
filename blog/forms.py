from django import forms
from tinymce.widgets import TinyMCE
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        # fields = ['title', 'text', 'image', 'show_post', 'tags', 'categories']
        fields = ['title', 'text', 'image', 'show_post']
        # widgets = {'text' : TinyMCE(attrs={'cols': 80, 'rows': 30, 'content_language':'fa'})}
        # widgets = {'text' : TinyMCE(attrs={'cols': 80, 'rows': 30})}
        widgets = {'text' : TinyMCE()}
