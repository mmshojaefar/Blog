from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from blog.models import Tag, Post_tag, User
from blog.forms import PostForm
from celery import shared_task
from bs4 import BeautifulSoup
from api.serializers import PostSerializer
import json

class ComplexEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, complex):
             return [obj.real, obj.imag]
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)


import re, io
from base64 import decodestring
from django.core.files import File


@shared_task
def create_post(request_post, request_file, username, tags):

    user = User.objects.get(username=username)
    form = PostForm(request_post)
    post = form.save(commit=False)
    post.post_send_time = timezone.now()
    post.user = user
    soup = BeautifulSoup(post.text, features="html.parser")
    post.safe_text = soup.get_text()
    
    image = bytes(request_file['image'], 'UTF-8')
    image = decodestring(image)
    img_io = io.BytesIO(image)
    post.image.save(request_file['name'], File(img_io))
    
    post.save()
    for tag in set(tags):
        selected_tag, _ = Tag.objects.get_or_create(name=tag)
        _, _ = Post_tag.objects.get_or_create(tag=selected_tag, post=post)
