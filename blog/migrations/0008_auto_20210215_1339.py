# Generated by Django 3.1.2 on 2021-02-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210209_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='checked_by_admin',
            field=models.BooleanField(default=False, verbose_name='پست برای تایید دیده شده است'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='post',
            name='show_post',
            field=models.BooleanField(default=True, verbose_name='آیا پست نمایش داده شود'),
        ),
    ]
