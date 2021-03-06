from django.urls import path
from . import views

urlpatterns = [
    path('posts/<str:username>/newpost/', views.newpost, name='newpost'),
    path('posts/<str:username>/<int:pk>/edit', views.editpost, name='editpost'),
    # path('profile/<str:pk>', views.profile, name='profile'), it is in account app
    path('posts/<str:username>/<int:pk>/', views.showpost, name='showpost'),
    path('', views.index, name='index'),
    path('category/', views.categorytree, name='categorytree'),
    path('category/<str:name>', views.showcategory, name='showcategory'),
    path('tag/<str:name>', views.showtag, name='showtag'),
    path('tags/', views.alltags, name='alltags'),

    path('api/likepost/', views.apilike, name='apilike'),
    path('api/likecomment/', views.apilikecomment, name='apilikecomment'),
    path('api/dislikepost/', views.apidislike, name='apidislike'),
    path('api/dislikecomment/', views.apidislikecomment, name='apidislikecomment'),
    path('api/acceptpost/', views.api_accept_post, name='api_accept_post'),
    path('api/acceptcomment/', views.api_accept_comment, name='api_accept_comment'),
    path('api/addtag/', views.add_tag, name='add_tag'),
    path('api/checkusername/', views.check_username, name='check_username'),
    path('api/gettag/', views.get_tag, name='get_tag'),
]
