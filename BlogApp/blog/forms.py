from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from .models import Post, Profile
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control btn alert-secondary',
        'placeholder': 'Введите пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control btn alert-secondary',
        'placeholder': 'Повторно введите пароль',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control btn alert-secondary',
                'placeholder': 'Логин',
            }),
            "first_name": TextInput(attrs={
                'class': 'form-control btn alert-secondary',
                'placeholder': 'Имя пользователя',
            }),
            "email": TextInput(attrs={
                'class': 'form-control btn alert-secondary',
                'placeholder': 'Адрес электронной почты'
            })
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
            }),
            "body": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            })
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')