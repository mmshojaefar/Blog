from django.db import models
from django.core.validators import RegexValidator
from tinymce import models as tinymce_models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    name = models.CharField(
        verbose_name='برچسب',
        max_length=100,
    )

    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    name = models.CharField(
        verbose_name='دسته بندی',
        max_length=100,
    )

    supercategories = models.ForeignKey(
        'Category',
        verbose_name='سر دسته',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

class Post(models.Model):
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        permissions = [
            ('accept_post', 'تایید کردن پست'),
        ]

    title = models.CharField(
        verbose_name='عنوان',
        max_length=200,
    )
    text = tinymce_models.HTMLField(
        verbose_name='متن',
    )
    image = models.ImageField(
        verbose_name='تصویر',
        blank=True,
        null=True,
        upload_to='post_imgs'
    )
    show_post = models.BooleanField(
        verbose_name='آیا پست نمایش داده شود',
        default=True,
    )
    post_send_time = models.DateTimeField(
        verbose_name='زمان ارسال پست',
    )
    accept_by_admin = models.BooleanField(
        verbose_name='پست تایید شده است',
        default=False,
    )
    # checked_by_admin = models.BooleanField(
    #     verbose_name='پست برای تایید دیده شده است',
    #     default=False,
    # )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='برچسب ها',
        through='Post_tag',
    )
    categories = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='دسته بندی ها',
    )
    post_likes = models.ManyToManyField(
        'User',
        verbose_name='پسندیدم',
        blank=True,
        related_name='post_like',
        through='Post_rating',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='post_user',
    )

    def __str__(self):
        return self.title

class Post_tag(models.Model):
    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

class Post_rating(models.Model):
    class Meta:
        verbose_name = 'پسندیدن/نپسندیدن پست'
        verbose_name_plural = 'پسندیدن/نپسندیدن پست ها'
        constraints = [
            models.UniqueConstraint(fields=['post','user'], name='rates'),
        ]

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    positive = models.BooleanField(
        verbose_name='پسندیدن؟'
    )

class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        permissions = [
            ('accept_comment', 'تایید کردن نظر'),
            # ('rate_comment', 'پسندیدن/نپسندیدن نظر'),
        ]
        ordering = ['-comment_send_time']
    
    text = models.CharField(
        verbose_name='متن',
        max_length=500,
    )
    accept_by_admin = models.BooleanField(
        verbose_name='کامنت تایید شده است',
        default=False,
    )
    # checked_by_admin = models.BooleanField(
    #     verbose_name='نظر برای تایید دیده شده است',
    #     default=False,
    # )
    comment_send_time = models.DateTimeField(
        verbose_name='زمان ارسال نظر',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='پست',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='comment_user',
    )
    comment_likes = models.ManyToManyField(
        'User',
        verbose_name='پسندیدم',
        blank=True,
        related_name='comment_like',
        through='Comment_rating',
    )

    def __str__(self):
        return str(self.text)[:50] + (len(self.text)>50)*'...'

class Comment_rating(models.Model):
    class Meta:
        verbose_name = 'پسندیدن/نپسندیدن نظر'
        verbose_name_plural = 'پسندیدن/نپسندیدن نظرات'

    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    positive = models.BooleanField(
        verbose_name='پسندیدن؟'
    )

class CustomUserManager(BaseUserManager):
    '''
    Custom user model manager where username is the unique identifiers for authentication
    '''
    def create_user(self, username, password, **extra_fields):
        '''
        Create and save a User with the given username and password.
        '''
        if not username:
            raise ValueError(ugettext_lazy('The Username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        '''
        Create and save a SuperUser with the given username and password.
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    # password = models.CharField(
    #     verbose_name=ugettext_lazy('رمز عبور'),
    #     max_length=128,
    # )
    username = models.CharField(
        verbose_name='نام کاربری',
        max_length=40,
        unique=True,
        primary_key=True,
    )
    first_name = models.CharField(
        verbose_name='نام',
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name='نام خانوداگی',
        max_length=100,
    )
    phone_regex = RegexValidator(
        regex=r'\b[0]{1}[9]{1}[0-9]{9}\b',
        message="شماره تلفن همراه باید به فرمت 09123456789 باشد",
    )
    phone = models.CharField(
        verbose_name='تلفن همراه',
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        unique=True,
    )
    birth_day = models.DateField(
        verbose_name='تاریخ تولد',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='تصویر',
        blank=True,
        null=True,
        upload_to='user_imgs'
    )
    date_joined = models.DateTimeField(
        verbose_name='زمان ثبت نام',
        blank=True,
        default=timezone.now,
    )
    # lastseen_time = models.DateTimeField(
    #     verbose_name='اخرین بازدید',
    #     blank=True,
    #     null=True,
    # )
    is_staff = models.BooleanField(
        verbose_name='کارمند است؟',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='فعال است؟',
        default=True,
    )
    is_superuser = models.BooleanField(
        verbose_name='ابرکاربر',
        default=False,
    )
    follow = models.ManyToManyField(
        'User',
        verbose_name='دنبال کنندگان',
        blank=True,
        through='Follow',
    )
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username + ' : ' + self.first_name + " " + self.last_name

class Follow(models.Model):
    class Meta:
        verbose_name = 'ارتباطات کاربران'
        verbose_name_plural = 'ارتباط کاربران'

    follower = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    followed = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='followed',
    )
