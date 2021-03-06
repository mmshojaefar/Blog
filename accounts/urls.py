from django.urls import path
from django.conf.urls import url
from . import views
from blog.views import register
from accounts import views

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
]