from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Blog, Comment
from django import forms

User = get_user_model()

class UpdateForm(UserChangeForm): 
    class Meta:
        model = User
        fields  = ("username","email","password")


class BlogForm(forms.ModelForm): 
    class Meta:
        model = Blog
        fields = ("title","description","image")

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "cols": 50, "placeholder": "Write your comment here..."})
        }
