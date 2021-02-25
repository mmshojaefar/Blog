# Generated by Django 3.1.2 on 2021-02-24 11:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True, verbose_name='نام کاربری')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوداگی')),
                ('phone', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='شماره تلفن همراه باید به فرمت 09123456789 باشد', regex='\\b[0]{1}[9]{1}[0-9]{9}\\b')], verbose_name='تلفن همراه')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_imgs', verbose_name='تصویر')),
                ('date_joined', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='زمان ثبت نام')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کارمند است؟')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال است؟')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='ابرکاربر')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='دسته بندی')),
                ('supercategories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='سر دسته')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='متن')),
                ('accept_by_admin', models.BooleanField(default=False, verbose_name='کامنت تایید شده است')),
                ('comment_send_time', models.DateTimeField(verbose_name='زمان ارسال نظر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'ordering': ['-comment_send_time'],
                'permissions': [('accept_comment', 'تایید کردن نظر')],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('text', tinymce.models.HTMLField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_imgs', verbose_name='تصویر')),
                ('show_post', models.BooleanField(default=True, verbose_name='آیا پست نمایش داده شود')),
                ('post_send_time', models.DateTimeField(verbose_name='زمان ارسال پست')),
                ('accept_by_admin', models.BooleanField(default=False, verbose_name='پست تایید شده است')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='دسته بندی ها')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'permissions': [('accept_post', 'تایید کردن پست')],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='برچسب')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
        migrations.CreateModel(
            name='Post_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tag')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
        migrations.CreateModel(
            name='Post_rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField(verbose_name='پسندیدن؟')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
            options={
                'verbose_name': 'پسندیدن/نپسندیدن پست',
                'verbose_name_plural': 'پسندیدن/نپسندیدن پست ها',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='post_likes',
            field=models.ManyToManyField(blank=True, related_name='post_like', through='blog.Post_rating', to='blog.User', verbose_name='پسندیدم'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(through='blog.Post_tag', to='blog.Tag', verbose_name='برچسب ها'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to='blog.user', verbose_name='کاربر'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='blog.user')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='blog.user')),
            ],
            options={
                'verbose_name': 'ارتباطات کاربران',
                'verbose_name_plural': 'ارتباط کاربران',
            },
        ),
        migrations.CreateModel(
            name='Comment_rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
            options={
                'verbose_name': 'پسندیدن/نپسندیدن نظر',
                'verbose_name_plural': 'پسندیدن/نپسندیدن نظرات',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_likes',
            field=models.ManyToManyField(blank=True, related_name='comment_like', through='blog.Comment_rating', to='blog.User', verbose_name='پسندیدم'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='پست'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to='blog.user', verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, through='blog.Follow', to='blog.User', verbose_name='دنبال کنندگان'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
