from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', related_name='forum_topics')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    views = models.IntegerField(default=0, verbose_name='浏览次数')

    def __str__(self):
        return self.title

    @property
    def post_count(self):
        return self.posts.count()

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_at']


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='所属帖子', related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', related_name='forum_posts')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return f'{self.author.username} - {self.topic.title}'

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = '回复'
        ordering = ['created_at']
