from rest_framework import routers
from api.views import CommentViewset, PostViewset

comment_router = routers.SimpleRouter()
comment_router.register('', CommentViewset, basename='comments')

post_router = routers.SimpleRouter()
post_router.register('', PostViewset, basename='posts')
