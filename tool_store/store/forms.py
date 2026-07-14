from django import forms
from .models import Tool


class ToolUploadForm(forms.Form):
    username = forms.CharField(max_length=150, label='用户名')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    name = forms.CharField(max_length=200, label='工具名称')
    description = forms.CharField(widget=forms.Textarea, label='工具描述')
    version = forms.CharField(max_length=50, label='版本号')
    file = forms.FileField(label='工具文件')
