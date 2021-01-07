from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30, label='Your Name')
    email = forms.EmailField(label='Your Email')
    to = forms.EmailField(label='To Email')
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)


class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'subtitle', 'body', 'tag', 'status')
