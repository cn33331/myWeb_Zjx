from django import forms
from .models import Topic, Post


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
