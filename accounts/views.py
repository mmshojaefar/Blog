from django.contrib.auth.decorators import login_required
from blog.models import Post, User
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.shortcuts import get_object_or_404
from blog.views import get_most_comment_posts
from .forms import settingsForm, PasswordResetForm
from blog.forms import UserForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import logging


logger = logging.getLogger(__name__)
    

def profile(request, username=None):
    """
    Summary:
        This function used to show profile page.
    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request
        username ([class str], optional): This variable represent the user's username for showing his/her profile!
                                       Defaults to None.

    Returns:
        [class HttpResponse]: It render profile page by rendering profile.html
    """
    if username == None:
        username = request.user.username
    logger.info(f'{username} trying to see profile page.')
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

@login_required
def settings(request):
    """
    Summary:
        This function used for change user data!

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It render settings form by rendering settings.html
    """
    logger.info(f'{request.user} send {request.method} request to settings.')
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

def register(request):
    """
    Summary:
        This function used for registering in the weblog and createing Standard User.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It render register form by rendering register.html
    """
    logger.info(f'someone send {request.method} request to settings.')
    if request.POST:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = timezone.now()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            std_user = Group.objects.get(name='کاربران عادی')
            std_user.user_set.add(user)
            print(user.username)
            # return HttpResponseRedirect(reverse('main_profile', kwargs={'username':user.username}))
            return HttpResponseRedirect(reverse('login'))
        else:
            form = UserForm(request.POST, request.FILES)
            return render(request, 'accounts/register.html', context={'form':form})
    form = UserForm()
    return render(request, 'accounts/register.html', context={'form':form})

class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
