# Generated by Django 3.1.2 on 2021-02-08 14:04

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210208_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=tinymce.models.HTMLField(verbose_name='متن'),
        ),
    ]
