# Generated by Django 3.1.2 on 2021-03-05 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210304_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='supercategories',
            new_name='supercategory',
        ),
    ]
