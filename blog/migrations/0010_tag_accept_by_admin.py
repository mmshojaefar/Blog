# Generated by Django 3.1.2 on 2021-03-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210305_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='accept_by_admin',
            field=models.BooleanField(default=False, verbose_name='برچسب تایید شده است'),
        ),
    ]
