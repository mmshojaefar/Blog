from django.urls import path
from django.conf.urls import url, include
from . import views
# from blog.views import register
from accounts import views
from accounts.views import MyPasswordResetView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='main_profile'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
]
