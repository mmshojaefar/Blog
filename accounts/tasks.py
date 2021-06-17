from __future__ import absolute_import, unicode_literals
from celery import shared_task
from blog.models import User
from django.contrib.auth.forms import PasswordResetForm


@shared_task
def send_mail(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    context['user'] = User.objects.get(username=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
