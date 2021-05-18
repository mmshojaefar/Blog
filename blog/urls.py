from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('popular/', views.popular, name='popular'),
    path('', views.index, name='index'),
    path('<str:username>/newpost/', views.newpost, name='newpost'),
    path('<str:username>/<int:pk>/edit/', views.editpost, name='editpost'),
    path('<str:username>/<int:pk>/', views.showpost, name='showpost'),
    path('category/', views.categorytree, name='categorytree'),
    path('category/<str:name>', views.showcategory, name='showcategory'),
    path('tag/<str:name>/', views.showtag, name='showtag'),
    path('tags/', views.alltags, name='alltags'),
    path('about/', views.aboutus, name='aboutus'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
