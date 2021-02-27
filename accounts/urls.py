from django.urls import path
from django.conf.urls import url
from . import views
from blog.views import register

urlpatterns = [
    # url(r'^password/$', views.change_password, name='change_password'),
    path('register/', register, name='register'),
]