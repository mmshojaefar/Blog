from django.urls import path
from . import views

urlpatterns = [
    path('newpost/',views.newpost, name='newpost'),
    path('posts/<int:pk>/',views.showpost, name='showpost'),
]
