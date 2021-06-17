from django import forms
from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Tag, Category, Post, User, Comment, Post_rating, Post_tag, Comment_rating, Follow
from django.contrib.auth.password_validation import validate_password

# Register your models here.

admin.site.register(Comment_rating)
admin.site.register(Post_rating)
admin.site.register(Post_tag)

class UserCreationForm(forms.ModelForm):
    '''
    A form for creating new users. Includes all the required fields, plus a repeated password.
    '''
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه و تکرار آن مطابقت ندارند ")
        validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    '''
    A form for updating users. Includes all the fields on the user, but replaces the password field with
    admin's password hash display field.
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser')
    # list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'birth_day', 'image', 'date_joined')}),
        ('دسترسی ها', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('گروه ها', {'fields': ('groups',)}),
    )
    
    search_fields = ('email','username','first_name', 'last_name')
    ordering = ('username',)
    # filter_horizontal = ()

admin.site.register(User, UserAdmin)



class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'accept_by_admin')
    actions = ['accepetـtag']
    search_fields = ['name',]
    list_filter = ('accept_by_admin',)

    def accepetـtag(self, request, queryset):
        updated = queryset.update(accept_by_admin=True)
        self.message_user(request, ngettext(
            '%d برچسب تایید شد.',
            '%d برچسب تایید شدند.',
            updated,
        ) % updated, messages.SUCCESS)

    accepetـtag.short_description = 'تایید تمام برچسب های انتخاب شده'

admin.site.register(Tag, TagAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'supercategory')
    search_fields = ['name',]

admin.site.register(Category, CategoryAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_text', 'accept_by_admin', 'post', 'get_user')
    actions = ['accepetـcomment']
    search_fields = ['user__username']
    list_filter = ('accept_by_admin',)
    ordering = ['post__title']

    def get_text(self, obj):
        return str(obj.text)[:40] + (len(obj.text)>40)*'...'
    get_text.short_description = 'نظر'

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'کاربر'


    def accepetـcomment(self, request, queryset):
        updated = queryset.update(accept_by_admin=True)
        self.message_user(request, ngettext(
            '%d نظر تایید شد.',
            '%d نظر تایید شدند.',
            updated,
        ) % updated, messages.SUCCESS)

    accepetـcomment.short_description = 'تایید تمام نظر های انتخاب شده'

admin.site.register(Comment, CommentAdmin)



class PostAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'accept_by_admin', 'show_post', 'get_user', 'categories')
    actions = ['accepetـpost']
    search_fields = ['safe_text']
    list_filter = ('accept_by_admin',)
    ordering = ['-post_send_time']

    def get_title(self, obj):
        return str(obj.title)[:40] + (len(obj.title)>40)*'...'
    get_title.short_description = 'عنوان پست'

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'کاربر'


    def accepetـpost(self, request, queryset):
        updated = queryset.update(accept_by_admin=True)
        self.message_user(request, ngettext(
            '%d پست تایید شد.',
            '%d پست تایید شدند.',
            updated,
        ) % updated, messages.SUCCESS)

    accepetـpost.short_description = 'تایید تمام پست های انتخاب شده'

admin.site.register(Post, PostAdmin)
