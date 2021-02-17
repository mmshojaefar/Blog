from django.http import HttpResponse, Http404
from django.shortcuts import render
from .forms import PostForm
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Post, Comment


# Create your views here.

@login_required
def newpost(request):
    ans = ''
    # username = request.user.username
    # username = request.user.get_username()
    # in template {{ user.get_username }}
    if request.POST:
        p_form = PostForm(request.POST)
        if p_form.is_valid():
            post = p_form.save(commit=False)
            post.post_send_time = timezone.now()
            # post.user = username
            # post.save()
            print(p_form['text'].value())
            ans = p_form['text'].value()
            # p_form.save_m2m()
            # go to /username/post_id
            # return HttpResponseRedirect(reverse('polls:user', args=(username, post.id)))
        else:
            p_form = PostForm(request.POST)
    else:
        p_form = PostForm()
    return render(request, 'blog/newpost.html', context={'form':p_form, 'ans':ans})


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
