# Generated by Django 3.1.2 on 2021-02-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210222_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=40, unique=True, verbose_name='نام کاربری'),
        ),
    ]
