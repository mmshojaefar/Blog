from django import template
from blog.models import Comment_rating, Post_rating, Comment

register = template.Library()

@register.filter(name='likes')
def likes(cm):
    return Comment_rating.objects.filter(positive=True, comment=cm).count()

@register.filter(name='dislikes')
def dislikes(cm):
    return Comment_rating.objects.filter(positive=False, comment=cm).count()

@register.filter(name='post_likes')
def post_likes(post):
    return Post_rating.objects.filter(positive=True, post=post).count()

@register.filter(name='post_dislikes')
def post_dislikes(post):
    return Post_rating.objects.filter(positive=False, post=post).count()

@register.filter(name='post_comments')
def post_comments(post):
    return Comment.objects.filter(post=post).count()


@register.filter(name='localTranslate')
def localTranslate(word):
    dictionary = {
        'title':'عنوان',
        'tag':'برچسب ها',
        'writer':'نویسندگان',
        'text':'متن',
    }
    return dictionary[word]
