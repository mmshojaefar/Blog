from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('likepost/', views.apilike, name='apilike'),
    path('likecomment/', views.apilikecomment, name='apilikecomment'),
    path('dislikepost/', views.apidislike, name='apidislike'),
    path('dislikecomment/', views.apidislikecomment, name='apidislikecomment'),
    path('acceptpost/', views.api_accept_post, name='api_accept_post'),
    path('acceptcomment/', views.api_accept_comment, name='api_accept_comment'),
    path('addtag/', views.add_tag, name='add_tag'),
    path('checkusername/', views.check_username, name='check_username'),
    path('gettag/', views.get_tag, name='get_tag'),
    path('getimage/', views.get_iamge, name='get_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
