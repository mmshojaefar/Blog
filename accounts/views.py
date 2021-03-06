# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from blog.models import Post
from django.shortcuts import render, redirect

def profile(request, username):
    owner = (request.user == username)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    posts = Post.objects.filter(user=username)
    print(owner, can_accept, posts)
    return render(request, 'registration/profile.html', context={'username':username,
                                                                 'can_accept':can_accept,
                                                                 'posts':posts,
                                                                  })
