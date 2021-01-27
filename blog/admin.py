from django.contrib import admin
from .models import Tag, Category, Post, User, Comment

# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
