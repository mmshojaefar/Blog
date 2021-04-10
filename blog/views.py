from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from django.http import JsonResponse
from blog.forms import PostForm, UserForm, SearchForm
from blog.models import Post_rating, Comment_rating, Post, Comment, Tag, User, Category, Post_tag
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q, Count
from bs4 import BeautifulSoup
import json

most_comment_posts = Post.objects.all() \
                .annotate(num_comments=Count('comment')) \
                .order_by('-num_comments')

# Create your views here.

# def index(request, whichpost=None):
def index(request):
    """
    Summary:
        This view used for main page. It show some post in some manner:
            - Latest posts posted
            - Most popular posts (Determine by likes and dislikes)
            - Most discussed (Determine by most comments)
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show the main page of blog by rendering index.html
    """
    form = SearchForm()

    # check search to determine show the main page or results
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # posts = Post.objects.none()
            allposts = Post.objects.filter(accept_by_admin=True)
            # print(form)
            data = form.cleaned_data['search']
            # print(data)

            # adv_search variable show we must search in anything or a specific field(it is not for search in period of time)
            adv_search = False
            adv_posts = {}
            

            # check for advanced search. if title, tag, writer, text or post_sent_time_from/to be in the request
            # it means that the user use advanced search

            print(request.GET['post_time_sent_from'])
            if 'post_time_sent_from' in request.GET and request.GET['post_time_sent_from']:
                allposts = allposts.filter(post_send_time__gte=request.GET['post_time_sent_from'])
                print(allposts)
            
            if 'post_time_sent_to' in request.GET and request.GET['post_time_sent_to']:
                allposts = allposts.filter(post_send_time__lte=request.GET['post_time_sent_to'])
                print(allposts)
            
            if 'title' in request.GET:
                title_filter = allposts.filter(title__icontains=data, accept_by_admin=True)
                # posts = (title_filter) | (posts)
                adv_posts['title'] = title_filter
                adv_search = True

            if 'tag' in request.GET:
                tag_filter = allposts.filter(tags__name__icontains=data, accept_by_admin=True)
                # posts = (tag_filter) | (posts)
                adv_posts['tag'] = tag_filter
                adv_search = True

            if 'writer' in request.GET:
                writer_filter = allposts.filter(user__username__icontains=data, accept_by_admin=True)
                # posts = (writer_filter) | (posts)
                adv_posts['writer'] = writer_filter
                adv_search = True

            if 'text' in request.GET:
                text_filter = allposts.filter(accept_by_admin=True).annotate(similarity=TrigramSimilarity('safe_text', data)).\
                                                    filter(similarity__gt=0.1).order_by('-similarity')
                # posts = (text_filter) | (posts)
                adv_posts['text'] = text_filter
                adv_search = True

            if not adv_search:
                print(data)
                print(allposts.filter(accept_by_admin=True))
                posts = allposts.filter(accept_by_admin=True).annotate(similarity=TrigramSimilarity('safe_text', data)).\
                                            filter(similarity__gt=0.1).order_by('-similarity')
                print(posts)
                return render(request, 'blog/index.html', 
                              context={'posts':posts, 'form':form, 'adv':False, 'most_comment_posts':most_comment_posts[:10]})
            else:
                # posts = posts.distinct()
                # print(adv_posts)
                return render(request, 'blog/index.html', 
                              context={'posts':adv_posts, 'form':form, 'adv':True, 'user':request.user, 'most_comment_posts':most_comment_posts[:10]})
        else:
            return render(request, 'blog/index.html', 
                          context={'form':form, 'user':request.user, 'most_comment_posts':most_comment_posts[:10]})
    else:
        posts = Post.objects.filter(accept_by_admin=True).order_by('-post_send_time').filter()[:5]
    return render(request, 'blog/index.html', 
                  context={'posts':posts, 'form':form, 'user':request.user, 'most_comment_posts':most_comment_posts[:10]})

def categorytree(request):
    """
    Summary:
        This view used to show all categories in form Tree view.
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show the category tree by rendering categorytree.html
    """
    categories = Category.objects.all()
    return render(request, 'blog/categorytree.html', context={'categories':categories, 'form':SearchForm()})

def showcategory(request, name):
    """
    Summary:
        This view used to show all post of a category that sorted by their send time.
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It shows the posts of geiven category by rendering showcategory.html.
                              If there is NOT any category with given name, it returns 404 not found.
    """
    get_object_or_404(Category, name=name)
    posts = Post.objects.filter(categories__name=name).order_by('-post_send_time')
    print(posts)
    return render(request, 'blog/showcategory.html', 
                  context={'posts':posts, 'category':name, 'form':SearchForm(), 'most_comment_posts':most_comment_posts[:10]})
 
def alltags(request):
    """
    Summary:
        Show all tags in beautiful manner.
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show all tags by rendering alltags.html
    """
    tags = Tag.objects.all().filter(accept_by_admin=True).order_by('name')
    return render(request, 'blog/alltags.html', context={'tags':tags, 'form':SearchForm()})

def showtag(request, name):
    """
    Summary:
        This view used to show all post of a tag that sorted by their send time.
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It shows the posts of geiven tag by rendering showtag.html.
                              If there is NOT any tag with given name, it returns 404 not found.
    """
    get_object_or_404(Tag, name=name)
    posts = Post.objects.filter(tags__name=name).order_by('-post_send_time')
    print(posts)
    return render(request, 'blog/showtag.html', 
                  context={'posts':posts, 'tag':name, 'form':SearchForm(), 'most_comment_posts':most_comment_posts[:10]})
 
@login_required
@permission_required('blog.add_post')
def newpost(request, username):
    """
    Summary:
        This function used for create new post! writer/editor/admin can add new posts. Each user can leave post if go to 
        blog/posts/<user name>/newpost
        When post created, The page will redirect to a page to show post! The owner(Writer of post) and editor/admin can
        see it before accepting by admin/editor. And owner can edit post before accepting by admin.
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request
        username ([class str]): This variable represent the user's username that create a new post! 

    Returns:
        [class HttpResponse]: It shows PostForm by rendering newpost.html
    """

    user = request.user
    if not user.username == username:
        return HttpResponseRedirect(reverse('newpost', kwargs={'username':request.user.username}))

    if request.POST:
        print(request.POST.getlist('tags'))           
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            tags = request.POST.getlist('tags')
            post.post_send_time = timezone.now()
            post.user = user
            soup = BeautifulSoup(post.text)
            post.safe_text = soup.get_text()
            print(safe_text)
            post.save()
            for tag in set(tags):
                selected_tag, _ = Tag.objects.get_or_create(name=tag)
                _, _ = Post_tag.objects.get_or_create(tag=selected_tag, post=post)
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, 'blog/newpost.html', context={'postForm':form, 'form':SearchForm()})

@permission_required('blog.change_post')
def editpost(request, username, pk):
    """
    Summary:
        This function used for edit a post! Only owner can edit the posts.
        If post accepted by admin, after editing the post, Other people cant see the post until editor/admin user accept
        the post again

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request
        username ([class str]): This variable represent the user's username that create a new post! 
        pk ([class int]): This variable represent the pk of post!

    Raises:
        Http404: [django.http.Http404]: It render 404 Not Found page. Http404 will raise when:
                                        1- A persron except owner want to edit the post.

    Returns:
        [class HttpResponse]: If username is the owner of post with given pk, owner can edits the post of geiven pk 
        by rendering editpost.html
    """
    # post = Post.objects.filter(pk=pk)
    # if not post.user.username == username:
    #     return HttpResponseRedirect(reverse('editpost', kwargs={'username':post.user.username, 'pk':post.pk}))
    user = request.user
    if not user.username == username:
        raise Http404
    if request.method=='GET':
        post = Post.objects.get(pk=pk)
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
            post.accept_by_admin = False
            tags = request.POST.getlist('tags')
            for tag in set(tags):
                selected_tag, _ = Tag.objects.get_or_create(name=tag)
                _, _ = Post_tag.objects.get_or_create(tag=selected_tag, post=post)

            post.save(update_fields=['title', 'text', 'image', 'show_post', 'categories', 'accept_by_admin'])
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':post.user.username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
            return render(request, 'blog/editpost.html', context={'form':form})
    # return render(request, 'blog/editpost.html', context={})

def showpost(request, username, pk):
    """
    Summary:
        This function used for showing post! Each post has a primary key(here is an id). Each post show in url below:
            blog/posts/post_id/
        The post show completely.
        Also all comments show in this page view.
        Each user (logged in or not) can see the post and comments(If the owner(writer of post) did not archive the post)
        but only logged in user can like/dislike post/comments.
        If the owner(writer of post) see this view, he/she see edit button and can edit post!
        Admin/editor user can see a button to accept the post/comments or reject accepted post/comments for public display
        also.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request
        username ([class str]): This variable represent the user's username that create a new post! 
        pk ([class int]): This variable represent the pk of post!

    Raises:
        Http404: [django.http.Http404]: It render 404 Not Found page. Http404 will raise when:
                                        1- Post is Not fot public display and the request is Not from owner
                                        2- Post is Not accepted and the request is Not from owner or editors or admins.

    Returns:
        [class HttpResponse]: If username is the owner of post with given pk, it shows the post of geiven pk 
        by rendering showpost.html
    """
    post = get_object_or_404(Post, pk=pk)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    owner = (request.user == post.user)
    if not post.show_post and not owner:
        raise Http404
    if (not can_accept) and (not owner) and (not post.accept_by_admin):
        raise Http404
    if not post.user.username == username:
        return HttpResponseRedirect(reverse('showpost', kwargs={'username':post.user.username, 'pk':post.pk}))    
    allcomments = post.comment_set.all()
    comments = allcomments.filter(accept_by_admin=True)
    likes = Post_rating.objects.filter(positive=True, post=post).count()
    dislikes = Post_rating.objects.filter(positive=False, post=post).count()
    return render(request, 'blog/showpost.html', context={'post':post,
                                                          'comments':comments,
                                                          'allcomments':allcomments,
                                                          'owner':owner,
                                                          'can_accept':can_accept,
                                                          'likes':likes,
                                                          'dislikes':dislikes,
                                                          'form': SearchForm(),
                                                          })

def register(request):
    """
    Summary:
        -----------

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It render register form by rendering register.html ----------------
    """
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
            form = UserForm(request.POST, request.FILES)
            return render(request, 'blog/register.html', context={'form':form})
    form = UserForm()
    return render(request, 'blog/register.html', context={'form':form})



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
                print(ptag.tag.accept_by_admin, ptag.tag)
                ptag.tag.accept_by_admin = True
                ptag.tag.save()

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
    tag = request.POST['tag']
    # result = Tag.objects.filter(name__icontains=tag).only("pk", "name")
    result = Tag.objects.filter(name__icontains=tag, accept_by_admin=True)
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

@require_http_methods(["POST"])
def get_tag(request):
    print('yesss')
    id = request.POST.get('id')
    post = Post.objects.get(pk=id)
    tags = Post_tag.objects.values_list('id', 'tag__name').filter(post=post)
    print(list(tags))
    return JsonResponse(data={'tags': list(tags)})
