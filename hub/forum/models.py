from django.db import models
from django.utils import timezone


class ForumUser(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    is_approved = models.BooleanField(default=False, verbose_name='是否已审核')
    apply_date = models.DateTimeField(default=timezone.now, verbose_name='申请日期')
    approved_date = models.DateTimeField(null=True, blank=True, verbose_name='审核日期')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '论坛用户'
        verbose_name_plural = '论坛用户'
        ordering = ['-apply_date']


class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, verbose_name='作者')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    views = models.IntegerField(default=0, verbose_name='浏览次数')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_at']


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='所属帖子')
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return f'{self.author.username} - {self.topic.title}'

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = '回复'
        ordering = ['created_at']