from django import urls
# from django.db import router
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from api.api_url_routers import comment_router, post_router


urlpatterns = [
    path('tags/', views.tags, name='apitag'),
    path('categories/', views.categories, name='apicategories'),
    path('comments/', include(comment_router.urls)),
    path('posts/', include(post_router.urls)),

    path('likepost/', views.apilike, name='apilike'),
    path('dislikepost/', views.apidislike, name='apidislike'),
    path('acceptpost/', views.api_accept_post, name='api_accept_post'),
    path('acceptcomment/', views.api_accept_comment, name='api_accept_comment'),
    path('likecomment/', views.apilikecomment, name='apilikecomment'),
    path('dislikecomment/', views.apidislikecomment, name='apidislikecomment'),
    path('addtag/', views.add_tag, name='add_tag'),
    path('checkusername/', views.check_username, name='check_username'),
    path('gettag/', views.get_tag, name='get_tag'),
    path('getimage/', views.get_iamge, name='get_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
