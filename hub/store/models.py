from django.db import models
from django.utils import timezone


class Tool(models.Model):
    name = models.CharField(max_length=200, verbose_name='工具名称')
    description = models.TextField(verbose_name='工具描述')
    version = models.CharField(max_length=50, verbose_name='版本号')
    file = models.FileField(upload_to='tools/', verbose_name='工具文件')
    upload_date = models.DateTimeField(default=timezone.now, verbose_name='上传时间')
    downloads = models.IntegerField(default=0, verbose_name='下载次数')

    def __str__(self):
        return f'{self.name} v{self.version}'

    class Meta:
        verbose_name = '工具'
        verbose_name_plural = '工具'
        ordering = ['-upload_date']
