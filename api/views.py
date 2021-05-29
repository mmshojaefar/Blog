from os import stat
from django.contrib.auth.models import Permission
from django.db.models.query import QuerySet
from django.http import JsonResponse
from blog.models import Post_rating, Comment_rating, Post, Comment, Tag, User, Category, Post_tag
from django.contrib.auth.decorators import login_required, permission_required
# from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.exceptions import ValidationError
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from .serializers import TagSerializers, CategorySerializer, CommentSerializer, PostSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status, viewsets, mixins
from django.shortcuts import get_object_or_404
from rest_framework.renderers import AdminRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import logging

logger = logging.getLogger(__name__)

@login_required()
@api_view(['POST'])
def apilike(request):
    logger.info(f'{request.user} send {request.method} request and like/remove dislike post id={request.data["post"]}')
    try:
        post = Post.objects.get(pk=request.data['post'])
    except Post.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

    try:
        like = Post_rating.objects.get(post=post, user=request.user)
    except Post_rating.DoesNotExist:
        like = Post_rating.objects.create(post=post, user=request.user, positive=True)
        return Response({'ok':'like'}, status=status.HTTP_201_CREATED)
    else:
        if like.positive == False:
            dislike = Post_rating.objects.get(post=post, user=request.user)
            dislike.delete()  
            return Response({'ok':'removedislike'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ok':'nothing'}, status=status.HTTP_208_ALREADY_REPORTED)

@login_required()
@api_view(['POST'])
def apidislike(request):
    logger.info(f'{request.user} send {request.method} request and dislike/remove like post id={request.data["post"]}')
    try:
        post = Post.objects.get(pk=request.data['post'])
    except Post.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)

    try:
        dislike = Post_rating.objects.get(post=post, user=request.user)
    except Post_rating.DoesNotExist:
        dislike = Post_rating.objects.create(post=post, user=request.user, positive=False)
        return Response({'ok':'dislike'}, status=status.HTTP_201_CREATED)
    else:
        if dislike.positive == True:
            like = Post_rating.objects.get(post=post, user=request.user)
            like.delete()  
            return Response({'ok':'removelike'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ok':'nothing'}, status=status.HTTP_208_ALREADY_REPORTED)

@permission_required('accept_post')
@api_view(['POST'])
def api_accept_post(request):
    logger.info(f'{request.user} send {request.method} request to change confirmness of post id={request.data["post"]}')
    try:
        post = Post.objects.get(pk=request.data['post'])
    except Post.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if not post.accept_by_admin:
            for ptag in Post_tag.objects.filter(post=post):
                ptag.tag.accept_by_admin = True
                ptag.tag.save()

    post.accept_by_admin = (not post.accept_by_admin)
    post.save()
    return Response({'ok':'ok'}, status=status.HTTP_206_PARTIAL_CONTENT)

@permission_required('accept_comment')
@api_view(['POST'])
def api_accept_comment(request):
    logger.info(f'{request.user} send {request.method} request to change confirmness of comment id={request.data["comment"]}')
    try:
        comment = Comment.objects.get(pk=request.data['comment'])
    except Comment.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
    comment.accept_by_admin = (not comment.accept_by_admin)
    comment.save()
    return Response({'ok':'ok'}, status=status.HTTP_206_PARTIAL_CONTENT)

@login_required()
@api_view(['POST'])
def apilikecomment(request):
    logger.info(f'{request.user} send {request.method} request and like/remove dislike comment id={request.data["comment"]}')
    try:
        comment = Comment.objects.get(pk=request.data['comment'])
    except Comment.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
    try:
        like = Comment_rating.objects.get(comment=comment, user=request.user)
    except Comment_rating.DoesNotExist:
        like = Comment_rating.objects.create(comment=comment, user=request.user, positive=True)
        return Response({'ok':'like'}, status=status.HTTP_201_CREATED)
    else:
        if like.positive == False:
            dislike = Comment_rating.objects.get(comment=comment, user=request.user)
            dislike.delete()
            return Response({'ok':'removedislike'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ok':'nothing'}, status=status.HTTP_208_ALREADY_REPORTED)

@login_required()
@api_view(['POST'])
def apidislikecomment(request):
    logger.info(f'{request.user} send {request.method} request and dislike/remove like comment id={request.data["comment"]}')
    try:
        comment = Comment.objects.get(pk=request.data['comment'])
    except Comment.DoesNotExist:
        return Response({'ok':'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
    try:
        dislike = Comment_rating.objects.get(comment=comment, user=request.user)
    except Comment_rating.DoesNotExist:
        dislike = Comment_rating.objects.create(comment=comment, user=request.user, positive=False)
        return Response({'ok':'dislike'}, status=status.HTTP_201_CREATED)
    else:
        if dislike.positive == True:
            like = Comment_rating.objects.get(comment=comment, user=request.user)
            like.delete()
            return Response({'ok':'removelike'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ok':'nothing'}, status=status.HTTP_208_ALREADY_REPORTED)

@login_required()
@api_view(['POST'])
def add_tag(request):
    logger.info(f'return all tag similar to {request.data["tag"]}. The request method is {request.method}')
    tag = request.data['tag']
    result = Tag.objects.filter(name__icontains=tag, accept_by_admin=True)
    return JsonResponse(data={'result': serializers.serialize("json" ,result)})

@api_view(['POST'])
def check_username(request):
    logger.info(f'check the username: {request.data["username"]} be unique. The request method is {request.method}')
    username = request.data['username']
    try:
        User.validate_username_custom(username)
    except ValidationError:
        return JsonResponse(data={'ok': None})
    else:
        num = User.objects.filter(username=username).count()
        if num == 0:
            return JsonResponse(data={'ok': True})
        return JsonResponse(data={'ok': False})

@api_view(['POST'])
def get_tag(request):
    logger.info(f'return all tags of post id={request.data.get("id")}. The request method is {request.method}.')
    id = request.data.get('id')
    post = Post.objects.get(pk=id)
    tags = Post_tag.objects.values_list('id', 'tag__name').filter(post=post)
    return JsonResponse(data={'tags': list(tags)})

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
@csrf_exempt
@api_view(['POST'])
def get_iamge(request):
    print(request.FILES)

@api_view(['GET', 'POST'])
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
def tags(request):
    if request.method == 'POST':
        new_tag = TagSerializers(data=request.data)
        if new_tag.is_valid():
            # Tag(name=new_tag.validated_data['name'], accept_by_admin=new_tag.validated_data['accept_by_admin']).save()
            new_tag.save()
            return Response({'created':'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response(new_tag.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tags = Tag.objects.all()
        serialized_tags = TagSerializers(tags, many=True)
        return Response(serialized_tags.data, status=status.HTTP_200_OK)

@api_view()
@renderer_classes([BrowsableAPIRenderer, AdminRenderer, JSONRenderer])
def categories(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    categories = Category.objects.all()
    result_page = paginator.paginate_queryset(categories, request)
    serialized_categories = CategorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serialized_categories.data)


class CommentViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [BrowsableAPIRenderer, AdminRenderer, JSONRenderer]

    def list(self, request):
        queryset = Comment.objects.all()
        comment_serialized = CommentSerializer(queryset, many=True)
        return Response(comment_serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        comment_serialized = CommentSerializer(comment)
        return Response(comment_serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        comment_serialized = CommentSerializer(data=request.data)
        if comment_serialized.is_valid():
            comment_serialized.save(request.user)
            return Response({'created':'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Comment.objects.all()
        comment_instance = get_object_or_404(queryset, pk=pk)
        comment_serialized = CommentSerializer(comment_instance, data=request.data)
        if comment_serialized.is_valid():
            comment_serialized.save(request.user)
            return Response({'updated':'ok'}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(comment_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Comment.objects.all()
        comment_instance = get_object_or_404(queryset, pk=pk)
        comment_serialized = CommentSerializer(comment_instance, data=request.data, partial=True)
        if comment_serialized.is_valid():
            comment_serialized.save(request.user)
            return Response({'partial updated':'ok'}, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(comment_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Comment.objects.all()
        comment_instance = get_object_or_404(queryset, pk=pk)
        comment_instance.delete();
        return Response({'deleted':'ok'}, status=status.HTTP_204_NO_CONTENT)


class PostViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [BrowsableAPIRenderer, AdminRenderer, JSONRenderer]

