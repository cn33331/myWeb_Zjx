from django.db import models
from django.utils import timezone


class TransferRecord(models.Model):
    PLATFORM_CHOICES = [
        ('airportal', 'AirPortal 空投'),
        ('wenshushu', '文叔叔'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='平台')
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='取件码')
    link = models.URLField(max_length=500, blank=True, null=True, verbose_name='取件链接')
    file_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='文件名')
    file_size = models.CharField(max_length=50, blank=True, null=True, verbose_name='文件大小')
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return f'{self.get_platform_display()} - {self.code or self.link or "无码"}'

    class Meta:
        verbose_name = '传输记录'
        verbose_name_plural = '传输记录'
        ordering = ['-created_at']
