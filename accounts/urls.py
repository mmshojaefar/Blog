from django.urls import path
from django.conf.urls import url
from . import views
from blog.views import register

urlpatterns = [
    path('register/', register, name='register'),
]