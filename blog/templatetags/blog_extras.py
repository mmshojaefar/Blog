from django import template
from blog.models import Comment_rating, Post_rating, Comment

register = template.Library()

@register.filter(name='persian_int')
def persian_int(english_int):
    persian_nums = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    english_int = str(english_int).split('،')[0]    # For showing only one time
                                                    # For example instead of showing
                                                    # یک روز و سه ساعت
                                                    # it shows یک روز
    number = str(english_int)
    persian_dict = number.maketrans(persian_nums)
    result = number.translate(persian_dict)
    return result

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
