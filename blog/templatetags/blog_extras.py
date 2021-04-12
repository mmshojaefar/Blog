from django import template
from blog.models import Comment_rating, Post_rating, Comment

register = template.Library()


@register.filter(name='persian_int')
def persian_int(english_int):
    persian_nums = {'0': '۰', '1': '۱', '2': '۲', '3': '۳',
                    '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    english_int = str(english_int).split('،')[0]    # For showing only one time
                                                    # For example instead of showing
                                                    # یک روز و سه ساعت
                                                    # it shows یک روز
    number = str(english_int)
    persian_dict = number.maketrans(persian_nums)
    result = number.translate(persian_dict)
    return result


@register.filter(name='comment_likes')
def comment_likes(cm):
    return Comment_rating.objects.filter(positive=True, comment=cm).count()


@register.filter(name='comment_dislikes')
def comment_dislikes(cm):
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
        'title': 'عنوان',
        'tag': 'برچسب ها',
        'writer': 'نویسندگان',
        'text': 'متن',
    }
    return dictionary[word]


@register.simple_tag
def is_liked_post_by_user(post, user, rate):
    if rate == 'like':
        positive = True
    elif rate == 'dislike':
        positive = False
    if user == None:
        return False
    result = Post_rating.objects.filter(
        post=post, user=user, positive=positive)
    return bool(result)


@register.simple_tag
def is_liked_comment_by_user(comment, user, rate):
    if rate == 'like':
        positive = True
    elif rate == 'dislike':
        positive = False
    if user == None:
        return False
    result = Comment_rating.objects.filter(
        comment=comment, user=user, positive=positive)
    return bool(result)
