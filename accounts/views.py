# from django import forms
from blog.models import Post, User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from blog.views import get_most_comment_posts
from .forms import settingsForm
from django.contrib import messages

def profile(request, username=None):
    if username == None:
        username = request.user.username
    get_object_or_404(User, username=username)
    owner = (request.user.username == username)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    posts = Post.objects.filter(user__username=username)
    return render(request, 'registration/profile.html', context={'username':username,
                                                                 'can_accept':can_accept,
                                                                 'posts':posts,
                                                                 'owner':owner,
                                                                 'most_comment_posts' : get_most_comment_posts()[:10],
                                                                })

def settings(request):
    if request.method == 'POST':
        form = settingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات با موفقیت ذخیره شد.', extra_tags='success')
        else:
            messages.error(request, 'متاسفانه خطایی رخ داد', extra_tags='danger')
            return render(request, 'accounts/settings.html', context={'form':form})
    else:
        form = settingsForm(instance=request.user)
    return render(request, 'accounts/settings.html', context={'form':form})
