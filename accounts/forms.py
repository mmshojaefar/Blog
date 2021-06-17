from django import forms
from blog.models import User
from accounts.tasks import send_mail
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore


class settingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'birth_day', 'image']


class PasswordResetForm(PasswordResetFormCore):
    email = forms.EmailField(max_length=254, widget=forms.TextInput())

    def send_mail(self, subject_template_name, email_template_name, context, 
                  from_email, to_email, html_email_template_name=None):
        
        context['user'] = context['user'].username
        
        send_mail.delay(subject_template_name=subject_template_name, 
                        email_template_name=email_template_name,
                        context=context,
                        from_email=from_email,
                        to_email=to_email,
                        html_email_template_name=html_email_template_name)
