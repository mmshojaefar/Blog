from django import template
from blog.models import Comment_rating

register = template.Library()

@register.filter(name='likes')
def likes(cm):
    return Comment_rating.objects.filter(positive=True, comment=cm).count()

@register.filter(name='dislikes')
def dislikes(cm):
    return Comment_rating.objects.filter(positive=False, comment=cm).count()

@register.filter(name='localTranslate')
def localTranslate(word):
    dictionary = {
        'title':'عنوان',
        'tag':'برچسب ها',
        'writer':'نویسندگان',
        'text':'متن',
    }
    return dictionary[word]
