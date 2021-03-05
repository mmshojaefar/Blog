from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from django.http import JsonResponse
from blog.forms import PostForm, UserForm
from blog.models import Post_rating, Comment_rating, Post, Comment, Tag, User, Category
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json


# Create your views here.

def index(request):
    posts = Post.objects.order_by('-post_send_time').filter()[:5]
    print(posts)
    return render(request, 'blog/index.html', context={'posts':posts})

def categorytree(request):
    categories = Category.objects.all()
    return render(request, 'blog/categorytree.html', context={'categories':categories})


@login_required
@permission_required('blog.add_post')
def newpost(request, username):
    '''
        This function used for create new post! writer/editor/admin can add new posts. Each user can leave post if go to 
        blog/posts/<user name>/newpost
        When post created, The page will redirect to a page to show post! The owner(Writer of post) and editor/admin can
        see it before accepting by admin/editor. And owner can edit post before accepting by admin.
    '''
    user = request.user
    if not user.username == username:
        return HttpResponseRedirect(reverse('newpost', kwargs={'username':request.user.username}))

    if request.POST:
        print(request.POST.getlist('tags'))
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_send_time = timezone.now()
            post.user = user
            post.save()
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, 'blog/newpost.html', context={'form':form})

@permission_required('blog.change_post')
def editpost(request, username, pk):
    '''
        This function used for edit a post! Only owner can edit the posts.
        If post accepted by admin, after editing the post, Other people cant see the post until editor/admin user accept
        the post again 
    '''
    user = request.user
    if not user.username == username:
        raise Http404
    # print(request.method=='GET')
    if request.method=='GET':
        post = Post.objects.get(pk=pk)
        # form = PostForm(initial={'title': post.title,
        #                         'text': post.text,
        #                         'image': post.image,
        #                         'show_post': post.show_post,
        #                         'categories': post.categories,
        #                         #  'tags': post.tags,
        #                         })
        form = PostForm(instance=post)
        return render(request, 'blog/editpost.html', context={'form':form})
    else:
        print(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.get(pk=pk)
            edited_post = form.save(commit=False)
            post.title = edited_post.title
            post.text = edited_post.text
            post.image = edited_post.image
            post.show_post = edited_post.show_post
            post.categories = edited_post.categories
            # post.tags = edited_post.tags
            post.accept_by_admin = False
            # post.save(update_fields=['title', 'text', 'image', 'show_post', 'categories', 'tags', 'accept_by_admin'])
            post.save(update_fields=['title', 'text', 'image', 'show_post', 'categories', 'accept_by_admin'])
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':post.user.username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
    return render(request, 'blog/editpost.html', context={})


def showpost(request, username, pk):
    '''
        This function used for showing post! Each post has a primary key(here is an id). Each post show in url below:
            blog/posts/post_id/
        The post show completely.
        Also all comments show in this page view.
        Each user (logged in or not) can see the post and comments(If the owner(writer of post) did not archive the post)
        but only logged in user can like/dislike post/comments.
        If the owner(writer of post) see this view, he/she see edit button and can edit post!
        Admin/editor user can see a button to accept the post/comments or reject accepted post/comments for public display
        also.
    '''
    post = get_object_or_404(Post, pk=pk)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    owner = (request.user == post.user)
    if not post.show_post and not owner:
        raise Http404
    if (not can_accept) and (not owner) and (not post.accept_by_admin):
        raise Http404
    allcomments = post.comment_set.all()
    comments = allcomments.filter(accept_by_admin=True)
    likes = Post_rating.objects.filter(positive=True, post=post).count()
    dislikes = Post_rating.objects.filter(positive=False, post=post).count()
    # print('-'*50)
    # print(likes)
    # print(allcomments)
    # print(comments)
    # print(can_accept)
    # print(owner)
    # print('-'*50)
    return render(request, 'blog/showpost.html', context={'post':post,
                                                          'comments':comments,
                                                          'allcomments':allcomments,
                                                          'owner':owner,
                                                          'can_accept':can_accept,
                                                          'likes':likes,
                                                          'dislikes':dislikes,
                                                          })


def register(request):
    if request.POST:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = timezone.now()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            std_user = Group.objects.get(name='کاربران عادی')
            std_user.user_set.add(user)
            # return HttpResponseRedirect(reverse('blog:profile', args=(user.username)))
            return HttpResponseRedirect(reverse('profile', args=(user.username)))
        else:
            form = UserForm(request.POST)
            return render(request, 'blog/register.html', context={'form':form})
    form = UserForm()
    return render(request, 'blog/register.html', context={'form':form})

# @csrf_exempt
# @require_http_methods(["POST"])
# def apilike(request):
#     print(request.POST)
#     return JsonResponse(data={'ok':True})

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

    post.accept_by_admin = (not post.accept_by_admin)
    post.save()
    return JsonResponse(data={'ok':'ok'})
    # return JsonResponse(data={})

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
    # return JsonResponse(data={})

@login_required()
@require_http_methods(["POST"])
def apilikecomment(request):
    try:
        comment = Comment.objects.get(pk=request.POST['comment'])
    except Comment.DoesNotExist:
        return JsonResponse(data={'ok':'NOT FOUND'})

    print(comment)
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
    # print(222222222222222222222)
    tag = request.POST['tag']
    # result = Tag.objects.filter(name__icontains=tag).only("pk", "name")
    result = Tag.objects.filter(name__icontains=tag)
    # print(result)
    # print(serializers.serialize("json" ,result))
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
        print(num)
        if num == 0:
            return JsonResponse(data={'ok': True})
        return JsonResponse(data={'ok': False})
