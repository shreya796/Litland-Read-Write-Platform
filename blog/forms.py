from django import forms

from .models import Post , Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post #will follow the Post Model
        fields = ( 'title' ,'text', 'category','published_date') #'publish', 'drafts')

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']
