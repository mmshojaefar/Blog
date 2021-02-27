from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, User
from django.contrib.auth.password_validation import validate_password

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'show_post', 'categories', 'tags']
        widgets = {'text' : TinyMCE()}

    def get_form(request):
        pass

class UserForm(forms.ModelForm):
    '''
    This form created for registering to the blog and each user is member of std_user group at first
    '''
    password=forms.CharField(
        label='رمزعبور',
        widget=forms.PasswordInput(),
    )
    confirm_password=forms.CharField(
        label='تکرار رمزعبور',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'birth_day', 'image', 'username', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Here we checked password and confirm password to be same and then do some validation to get strong password
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("رمزعبور و تکرار آن مطابقت ندارند.")
        validate_password(password)
