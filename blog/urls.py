from django.urls import path
from . import views

urlpatterns = [
    path('posts/<str:username>/newpost/', views.newpost, name='newpost'),
    path('posts/<str:username>/<int:pk>/edit', views.editpost, name='editpost'),
    # path('register/', views.register, name='register'),
    # path('profile/<str:pk>', views.profile, name='profile'),
    path('posts/<str:username>/<int:pk>/', views.showpost, name='showpost'),
    path('api/likepost/', views.apilike, name='apilike'),
    path('api/dislikepost/', views.apidislike, name='apidislike'),
    path('api/acceptpost/', views.api_accept_post, name='api_accept_post'),
]
