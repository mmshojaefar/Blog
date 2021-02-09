from django.http import HttpResponse
from django.shortcuts import render
from .forms import PostForm
from tinymce.views import render_to_link_list
from unicodedata import bidirectional
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone


# Create your views here.

# @login_required
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
