from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import PostForm, UserForm
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from django.contrib.auth.models import Group


# Create your views here.

@login_required
def newpost(request):
    username = request.user
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_send_time = timezone.now()
            post.user = username
            post.save()
            # print(p_form['text'].value())
            # ans = p_form['text'].value()
            # return HttpResponseRedirect(reverse('polls:user', args=(username, post.id)))
        else:
            form = PostForm(request.POST)
    else:
        print(1111111111111111111)
        form = PostForm()
    return render(request, 'blog/newpost.html', context={'form':form})


def showpost(request, pk):
    '''
        This function used for showing post! Each post has a primary key(here is an id). Each post show in url below:
            blog/posts/post_id/
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        The post show completely.
        Also all comments show in this page view.
        Each user (logged in or not) can see the post and comments but only logged in user can like/dislike post/comments.
        If the writer of post/editor/admin see this view, They see edit button and can edit post!
    '''
    post = get_object_or_404(Post, pk=pk)
    print(post.accept_by_admin)
    if not post.accept_by_admin:
        raise Http404
    comments = post.comment_set.filter(accept_by_admin=True)
    print('---------------------')
    print(comments)
    print('---------------------')
    return render(request, 'blog/showpost.html', context={'post':post, 'comments':comments})


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
        else:
            form = UserForm(request.POST)
            return render(request, 'blog/register.html', context={'form':form})
    form = UserForm()
    return render(request, 'blog/register.html', context={'form':form})

