# Generated by Django 3.1.2 on 2021-02-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210222_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_day',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
    ]
