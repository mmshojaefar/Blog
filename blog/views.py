from django.http import HttpResponse, Http404
from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import PostForm, UserForm
from .models import Post_rating
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from django.contrib.auth.models import Group


# Create your views here.

@login_required
@permission_required('blog.add_post')
def newpost(request, username):
    '''
        This function used for create new post! writer/editor/admin can add new posts. Each user can leave post if go to 
        blog/posts/<user name>/newpost
    '''
    user = request.user
    if not user.username == username:
        return HttpResponseRedirect(reverse('newpost', kwargs={'username':request.user.username}))

    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_send_time = timezone.now()
            post.user = user
            post.save()
            return HttpResponseRedirect(reverse('showpost', kwargs={'username':username.username, 'pk':post.pk}))
        else:
            form = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, 'blog/newpost.html', context={'form':form})

# @permission_required('blog.change_post')
def editpost(request, username, pk):
    '''
        This function used for edit a post! Only owner can edit the posts.
    '''
    user = request.user
    if not user.username == username:
        raise Http404
    # print(request.method=='GET')
    if request.method=='GET':
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title': post.title,
                                'text': post.text,
                                'image': post.image,
                                'show_post': post.show_post,
                                'categories': post.categories,
                                #  'tags': post.tags,
                                })
        # , 'text', 'image', 'show_post', 'categories', 'tags')
        return render(request, 'blog/editpost.html', context={'form':form})
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
            post.save()
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
        Each user (logged in or not) can see the post and comments but only logged in user can like/dislike post/comments.
        If the writer of post/editor/admin see this view, They see edit button and can edit post!
        Admin/editor user can see a button to accept the post for public display also.
    '''
    post = get_object_or_404(Post, pk=pk)
    can_accept =  request.user.groups.filter(name='مدیران').exists() or request.user.groups.filter(name='ویراستاران').exists()
    owner = (request.user == post.user)
    if (not can_accept) and (not owner) and (not post.accept_by_admin):
        raise Http404
    allcomments = post.comment_set.all()
    comments = allcomments.filter(accept_by_admin=True)
    likes = Post_rating.objects.filter(positive=True, post=post).count()
    dislikes = Post_rating.objects.filter(positive=False, post=post).count()
    print('---------------------')
    print(likes)
    print(allcomments)
    print(comments)
    print(can_accept)
    print(owner)
    print('---------------------')
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
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = timezone.now()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            std_user = Group.objects.get(name='کاربران عادی')
            std_user.user_set.add(user)
            return HttpResponseRedirect(reverse('blog:profile', args=(user.username)))
        else:
            form = UserForm(request.POST)
            return render(request, 'blog/register.html', context={'form':form})
    form = UserForm()
    return render(request, 'blog/register.html', context={'form':form})

