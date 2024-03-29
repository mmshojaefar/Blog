from datetime import datetime, time
from django.shortcuts import redirect, render, HttpResponseRedirect, reverse, Http404
from blog.forms import PostForm, UserForm, SearchForm
from blog.models import Post_rating, Comment_rating, Post, Comment, Tag, User, Category, Post_tag
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import Group
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages
from django.db.models import Q, Count
from bs4 import BeautifulSoup
from blog.tasks import create_post
from base64 import encodebytes
import json
import logging

logger = logging.getLogger(__name__)

def get_most_comment_posts():
    logger.info('get most comment posts')
    most_comment_posts = Post.objects.filter(accept_by_admin=True, show_post=True) \
                    .annotate(num_comments=Count('comment')) \
                    .order_by('-num_comments')
    return most_comment_posts

# Create your views here.

def index(request):
    """
    Summary:
        This view used for main page. It show some post in some manner:
            - Latest posts posted
            - Most discussed post(Determine by most comments) in sidebar
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show the main page of blog by rendering index.html
    """
    logger.info(f'load index page. search form:{"search" in request.GET}')
    form = SearchForm()

    # check search to determine show the main page or results
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            allposts = Post.objects.filter(accept_by_admin=True, show_post=True)
            data = form.cleaned_data['search']

            # adv_search variable show we must search in anything or a specific field(it is not for search in period of time)
            adv_search = False
            adv_posts = {}            

            # check for advanced search. if title, tag, writer, text or post_sent_time_from/to be in the request
            # it means that the user use advanced search
            if 'post_time_sent_from' in request.GET and request.GET['post_time_sent_from']:
                allposts = allposts.filter(post_send_time__gte=request.GET['post_time_sent_from'])
            
            if 'post_time_sent_to' in request.GET and request.GET['post_time_sent_to']:
                allposts = allposts.filter(post_send_time__lte=request.GET['post_time_sent_to'])
            
            if 'title' in request.GET:
                title_filter = allposts.filter(title__icontains=data, accept_by_admin=True)
                adv_posts['title'] = title_filter
                adv_search = True

            if 'tag' in request.GET:
                tag_filter = allposts.filter(tags__name__icontains=data, accept_by_admin=True)
                adv_posts['tag'] = tag_filter
                adv_search = True

            if 'writer' in request.GET:
                writer_filter = allposts.filter(user__username__icontains=data, accept_by_admin=True)
                adv_posts['writer'] = writer_filter
                adv_search = True

            if 'text' in request.GET:
                text_filter = allposts.filter(accept_by_admin=True).annotate(similarity=TrigramSimilarity('safe_text', data)).\
                                                    filter(similarity__gt=0.1).order_by('-similarity')
                adv_posts['text'] = text_filter
                adv_search = True

            if not adv_search:
                posts = allposts.annotate(similarity=TrigramSimilarity('safe_text', data)).\
                                            filter(similarity__gt=0.1).order_by('-similarity')
                return render(request, 'blog/index.html', 
                              context={'posts':posts, 'form':form, 'adv':False, 'most_comment_posts':get_most_comment_posts()[:10]})
            else:
                return render(request, 'blog/index.html', 
                              context={'posts':adv_posts, 'form':form, 'adv':True, 'user':request.user, 'most_comment_posts':get_most_comment_posts()[:10]})
        else:
            return render(request, 'blog/index.html', 
                          context={'form':form, 'user':request.user, 'most_comment_posts':get_most_comment_posts()[:10]})
    else:
        posts = Post.objects.filter(accept_by_admin=True, show_post=True).order_by('-post_send_time').filter()[:10]
    return render(request, 'blog/index.html', 
                  context={'posts':posts, 'form':form, 'user':request.user, 'most_comment_posts':get_most_comment_posts()[:10]})

def popular(request):
    """
    Summary:
        This view used for main page. It show some post in some manner:
            - Most popular posts (Determine by likes)
            - Most discussed post(Determine by most comments) in sidebar
        The search form also placed at the above.

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show the main page of blog by rendering index.html
    """
    logger.info('load popular page.')
    form = SearchForm()
    # get post with most likes in descending order.
    allposts = Post_rating.objects.filter(post__accept_by_admin=True, post__show_post=True)
    most_liked_post = allposts.filter(positive=True).values('post').annotate(count=Count('post')).order_by('-count')[:10]

    # store the pk of this posts in posts_pk list
    posts_pk = []
    for post in most_liked_post:
        posts_pk.append(post['post'])
    unordered_posts = Post.objects.filter(pk__in=posts_pk)
    
    # sort the posts by number of likes!
    posts = sorted(unordered_posts, key=lambda post: posts_pk.index(post.pk) )

    return render(request, 'blog/index.html', 
                  context={'posts':posts, 'form':form, 'user':request.user, 'most_comment_posts':get_most_comment_posts()[:10]})

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
    logger.info('load category tree page.')
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
    logger.info(f'load specified category({name}) page.')
    get_object_or_404(Category, name=name)
    posts = Post.objects.filter(categories__name=name, accept_by_admin=True, show_post=True).order_by('-post_send_time')
    return render(request, 'blog/showcategory.html', 
                  context={'posts':posts, 'category':name, 'form':SearchForm(), 'most_comment_posts':get_most_comment_posts()[:10]})
 
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
    logger.info('load all tags page.')
    tags = Tag.objects.filter(accept_by_admin=True).order_by('name')
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
    logger.info(f'load specified tag({name}) page.')
    get_object_or_404(Tag, name=name)
    posts = Post.objects.filter(tags__name=name, accept_by_admin=True, show_post=True).order_by('-post_send_time')
    return render(request, 'blog/showtag.html', 
                  context={'posts':posts, 'tag':name, 'form':SearchForm(), 'most_comment_posts':get_most_comment_posts()[:10]})
 
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

    logger.info(f'{request.user} want to create new post. request method is {request.method}')
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST['scheduledMessage']:
                tags = request.POST.getlist('tags')
                scheduledMessage = request.POST.getlist('scheduledMessage')
                scheduled_post = timezone.make_aware(datetime.strptime(' '.join(scheduledMessage), '%Y-%m-%d %H:%M'))
                if scheduled_post < timezone.now():
                    eta = timezone.now() + timezone.timedelta(minutes=1)
                else:
                    eta = scheduled_post
                create_post.apply_async((request.POST, 
                                         {
                                            'image':encodebytes(request.FILES['image'].read()).decode('utf-8'), 
                                            'name': str(request.FILES['image'])
                                         },
                                         request.user.username, 
                                         tags),
                                         eta =  eta)
                return HttpResponseRedirect(reverse('profile',))
            else:
                post = form.save(commit=False)
                tags = request.POST.getlist('tags')
                post.post_send_time = timezone.now()
                post.user = user
                soup = BeautifulSoup(post.text, features="html.parser")
                post.safe_text = soup.get_text()
                post.save()
                for tag in set(tags):
                    selected_tag, _ = Tag.objects.get_or_create(name=tag)
                    _, _ = Post_tag.objects.get_or_create(tag=selected_tag, post=post)
                return HttpResponseRedirect(reverse('showpost', kwargs={'username':username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST, request.FILES)
    else:
        form = PostForm()
    form = PostForm()
    return render(request, 'blog/newpost.html', context={'postForm':form, 'form':SearchForm()})

@permission_required('blog.change_post')
def editpost(request, username, pk):
    """
    Summary:
        This function used for edit a post! Only owner can edit the posts.
        If post accepted by admin, after editing the post, Other people cant see the post until editor/admin user accept
        the post again.
        The search form also placed at the above.

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
    logger.info(f'{request.user} want to edit post id={pk}. request method is {request.method}')
    user = request.user

    post = get_object_or_404(Post, pk=pk)
    if not user.username == username:
        raise Http404
    if post.user != user:
        raise Http404
    if request.method=='GET':
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(request, 'blog/editpost.html', context={'editform':form, 'form':SearchForm()})
    else:
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
            Post_tag.objects.filter(post=post).delete();
            for tag in set(tags):
                selected_tag, _ = Tag.objects.get_or_create(name=tag)
                _, _ = Post_tag.objects.get_or_create(tag=selected_tag, post=post)

            post.save(update_fields=['title', 'text', 'image', 'show_post', 'categories', 'accept_by_admin'])
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':post.user.username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
            return render(request, 'blog/editpost.html', context={'form':form})

def showpost(request, username, pk):
    """
    Summary:
        This function used for showing post! Each post has a primary key(here is an id). Each post show in url below:
            blog/posts/post_id/
        The post show completely.
        Also all comments show in this page view.
        If someone try to submit comment, the comment text will send to this function. It will save after validating test.
        Each user (logged in or not) can see the post and comments(If the owner(writer of post) did not archive the post)
        but only logged in user can like/dislike post/comments.
        If the owner(writer of post) see this view, he/she see edit button and can edit post!
        Admin/editor user can see a button to accept the post/comments or reject accepted post/comments for public display
        also.
        The search form also placed at the above.

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
    logger.info(f'show post id={pk} to {request.user}')
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
    tags = post.tags.all()
    context = {
        'post':post,
        'allcomments':allcomments,
        'owner':owner,
        'can_accept':can_accept,
        'tags' : tags,
        'form': SearchForm(),
    }
    if request.POST:
        text = request.POST['newComment']
        if len(text)>500:
            messages.error(request, 'نظر باید حداکثر 500 کاراکتر باشد.', extra_tags='danger')
        else:
            comment_send_time = datetime.now()
            user = request.user
            Comment.objects.create(text=text,
                                   comment_send_time=comment_send_time,
                                   post=post,
                                   user=user)
    
        return HttpResponseRedirect(reverse('showpost', kwargs={'username':post.user.username, 'pk':post.pk}))
    return render(request ,'blog/showpost.html', context=context)

def aboutus(request):
    """
    Summary:
        Showing a html page that there is some information in it to know more about us!

    Args:
        request ([class HttpRequest]): It is an HttpRequest object which is typically named request. It contains metadata 
                                       about the request

    Returns:
        [class HttpResponse]: It show some information about us by rendering aboutus.html
    """
    return render(request, 'blog/aboutus.html')
