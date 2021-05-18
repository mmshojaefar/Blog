from django.http import JsonResponse
from blog.models import Post_rating, Comment_rating, Post, Comment, Tag, User, Category, Post_tag
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.exceptions import ValidationError
import json


@login_required()
@require_http_methods(["POST"])
def apilike(request):
    try:
        post = Post.objects.get(pk=request.POST['post'])
    except Post.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})

    try:
        like = Post_rating.objects.get(post=post, user=request.user)
    except Post_rating.DoesNotExist:
        like = Post_rating.objects.create(post=post, user=request.user, positive=True)
        return JsonResponse(data={'ok':'like'})
    else:
        if like.positive == False:
            dislike = Post_rating.objects.get(post=post, user=request.user)
            dislike.delete()  
            return JsonResponse(data={'ok':'removedislike'})
    return JsonResponse(data={'ok':'nothing'})

@login_required()
@require_http_methods(["POST"])
def apidislike(request):
    try:
        post = Post.objects.get(pk=request.POST['post'])
    except Post.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})

    try:
        dislike = Post_rating.objects.get(post=post, user=request.user)
    except Post_rating.DoesNotExist:
        dislike = Post_rating.objects.create(post=post, user=request.user, positive=False)
        return JsonResponse(data={'ok':'dislike'})
    else:
        if dislike.positive == True:
            like = Post_rating.objects.get(post=post, user=request.user)
            like.delete()  
            return JsonResponse(data={'ok':'removelike'})
    return JsonResponse(data={'ok':'nothing'})

@permission_required('accept_post')
@require_http_methods(["POST"])
def api_accept_post(request):
    try:
        post = Post.objects.get(pk=request.POST['post'])
    except Post.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})
    else:
        if not post.accept_by_admin:
            for ptag in Post_tag.objects.filter(post=post):
                ptag.tag.accept_by_admin = True
                ptag.tag.save()

    post.accept_by_admin = (not post.accept_by_admin)
    post.save()
    return JsonResponse(data={'ok':'ok'})

@permission_required('accept_comment')
@require_http_methods(["POST"])
def api_accept_comment(request):
    try:
        comment = Comment.objects.get(pk=request.POST['comment'])
    except Comment.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})
    comment.accept_by_admin = (not comment.accept_by_admin)
    comment.save()
    return JsonResponse(data={'ok':'ok'})

@login_required()
@require_http_methods(["POST"])
def apilikecomment(request):
    try:
        comment = Comment.objects.get(pk=request.POST['comment'])
    except Comment.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})

    try:
        like = Comment_rating.objects.get(comment=comment, user=request.user)
    except Comment_rating.DoesNotExist:
        like = Comment_rating.objects.create(comment=comment, user=request.user, positive=True)
        return JsonResponse(data={'ok':'like'})
    else:
        if like.positive == False:
            dislike = Comment_rating.objects.get(comment=comment, user=request.user)
            dislike.delete()  
            return JsonResponse(data={'ok':'removedislike'})
    return JsonResponse(data={'ok':'nothing'})

@login_required()
@require_http_methods(["POST"])
def apidislikecomment(request):
    try:
        comment = Comment.objects.get(pk=request.POST['comment'])
    except Comment.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})

    try:
        dislike = Comment_rating.objects.get(comment=comment, user=request.user)
    except Comment_rating.DoesNotExist:
        dislike = Comment_rating.objects.create(comment=comment, user=request.user, positive=False)
        return JsonResponse(data={'ok':'dislike'})
    else:
        if dislike.positive == True:
            like = Comment_rating.objects.get(comment=comment, user=request.user)
            like.delete()
            return JsonResponse(data={'ok':'removelike'})
    return JsonResponse(data={'ok':'nothing'})

@require_http_methods(["POST"])
def add_tag(request):
    tag = request.POST['tag']
    # result = Tag.objects.filter(name__icontains=tag).only("pk", "name")
    result = Tag.objects.filter(name__icontains=tag, accept_by_admin=True)
    return JsonResponse(data={'result': serializers.serialize("json" ,result)})

@require_http_methods(["POST"])
def check_username(request):
    username = request.POST['username']
    try:
        User.validate_username_custom(username)
    except ValidationError:
        return JsonResponse(data={'ok': None})
    else:
        num = User.objects.filter(username=username).count()
        if num == 0:
            return JsonResponse(data={'ok': True})
        return JsonResponse(data={'ok': False})

@require_http_methods(["POST"])
def get_tag(request):
    print('yesss')
    id = request.POST.get('id')
    post = Post.objects.get(pk=id)
    tags = Post_tag.objects.values_list('id', 'tag__name').filter(post=post)
    return JsonResponse(data={'tags': list(tags)})

@require_http_methods(["POST"])
def get_iamge(request):
    print(request.FILES)
    print(11111111111111111111111111111)
