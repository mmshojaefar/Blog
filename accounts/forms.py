from django import forms
from blog.models import User

class settingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'birth_day', 'image']
