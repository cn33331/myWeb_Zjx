from django import forms
from .models import ForumUser, Topic, Post


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '用户名'})
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': '密码'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': '邮箱'})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '用户名'})
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': '密码'})
    )


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '帖子标题'}),
            'content': forms.Textarea(attrs={'placeholder': '帖子内容', 'rows': 8}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '回复内容', 'rows': 4}),
        }