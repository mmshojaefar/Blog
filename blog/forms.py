from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, User
from django.contrib.auth.password_validation import validate_password


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        label='جستجو',
    )
    post_time_sent_from = forms.DateTimeField(
        required=False,
        label='از',
    )
    post_time_sent_to = forms.DateTimeField(
        required=False,
        label='تا',
    )
    title = forms.BooleanField(
        required=False,
        label='عنوان',
    )
    text = forms.BooleanField(
        required=False,
        label='متن',
    )
    tag = forms.BooleanField(
        required=False,
        label='برچسب',
    )
    writer = forms.BooleanField(
        required=False,
        label='نویسنده',
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'text', 'categories', 'show_post']
        widgets = {'text' : TinyMCE()}


class UserForm(forms.ModelForm):
    '''
    This form created for registering to the blog and each user is member of std_user group at first
    '''
    password=forms.CharField(
        label='گذرواژه',
        widget=forms.PasswordInput(),
    )
    confirm_password=forms.CharField(
        label='تکرار گذرواژه',
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
            raise forms.ValidationError("گذرواژه و تکرار آن مطابقت ندارند.")
        validate_password(password)
