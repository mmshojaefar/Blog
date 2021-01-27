from django.db import models
# from django.core.validators import RegexValidator

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

    def __str__(self):
        return self.name

class Post(models.Model):
    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    title = models.CharField(
        verbose_name='عنوان',
        max_length=200,
    )
    text = models.CharField(
        verbose_name='متن',
        max_length=2000,
    )
    image = models.CharField(
        verbose_name='تصویر',
        blank=True,
        null=True,
        max_length=200,
    )
    video = models.CharField(
        verbose_name='ویدئو',
        blank=True,
        null=True,
        max_length=200,
    )
    show_post = models.BooleanField(
        verbose_name='نمایش داده شود',
        default=True,
    )
    post_send_time = models.DateTimeField(
        verbose_name='زمان ارسال پست',
    )
    accept_by_admin = models.BooleanField(
        verbose_name='پست تایید شده است',
        default=False,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='برچسب ها',
    )
    categories = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='دسته بندی ها',
    )
    post_like = models.ManyToManyField(
        'User',
        verbose_name='پسندیدم',
        blank=True,
        # null=True,
        related_name='post_like',
    )
    post_dislike = models.ManyToManyField(
        'User',
        verbose_name='نپسندیدم',
        blank=True,
        # null=True,
        related_name='post_dislike',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='post_user',
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
    
    text = models.CharField(
        verbose_name='متن',
        max_length=500,
    )
    accept_by_admin = models.BooleanField(
        verbose_name='کامنت تایید شده است',
        default=False,
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
    comment_like = models.ManyToManyField(
        'User',
        verbose_name='پسندیدم',
        blank=True,
        # null=True,
        related_name='comment_like',
    )
    comment_dislike = models.ManyToManyField(
        'User',
        verbose_name='نپسندیدم',
        blank=True,
        # null=True,
        related_name='comment_dislike'
    )

    def __str__(self):
        return self.text[:50] + '...'

class User(models.Model):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    first_name = models.CharField(
        verbose_name='نام',
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name='نام خانوداگی',
        max_length=100,
    )
    # phone_regex = RegexValidator(
    #     regex=r'\b[0]{1}[9]{1}[0-9]{9}\b',
    #     message="شماره تلفن همراه باید به فرمت 09123456789 باشد"
    # )
    phone = models.CharField(
        verbose_name='تلفن همراه',
        # validators=[phone_regex],
        max_length=17,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        unique=True,
    )
    image = models.CharField(
        verbose_name='تصویر',
        blank=True,
        null=True,
        max_length=200,
    )
    register_time = models.DateField(
        verbose_name='زمان ثبت نام',
        blank=True,
    )
    register_time = models.DateTimeField(
        verbose_name='اخرین بازدید',
        blank=True,
    )
    follow = models.ManyToManyField(
        'User',
        verbose_name='دنبال کنندگان',
        blank=True,
        # null=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
