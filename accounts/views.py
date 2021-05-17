# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from blog.models import Post, User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from blog.views import most_comment_posts

def profile(request, username=None):
    # print(type(request)) #class 'django.core.handlers.wsgi.WSGIRequest'
    # print(request) #WSGIRequest: GET '/accounts/profile/'
    if username == None:
        username = request.user.username
    get_object_or_404(User, username=username)
    print(username)
    owner = (request.user.username == username)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    posts = Post.objects.filter(user__username=username)
    print(owner, can_accept, posts)
    return render(request, 'registration/profile.html', context={'username':username,
                                                                 'can_accept':can_accept,
                                                                 'posts':posts,
                                                                 'most_comment_posts' : most_comment_posts,
                                                                })
