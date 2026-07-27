from django.db import models
from django.utils import timezone


class NoteRepository(models.Model):
    REPO_TYPE_CHOICES = [
        ('local', '本地仓库'),
        ('remote', '远程仓库'),
    ]
    
    name = models.CharField(max_length=100)
    repo_type = models.CharField(max_length=20, choices=REPO_TYPE_CHOICES, default='remote')
    repo_url = models.CharField(max_length=500, blank=True)
    local_path = models.CharField(max_length=500)
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(max_length=50, default='idle')
    sync_message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '笔记仓库'
        verbose_name_plural = '笔记仓库'

    def __str__(self):
        return self.name


class NoteFile(models.Model):
    repository = models.ForeignKey(NoteRepository, on_delete=models.CASCADE, related_name='notes')
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=200)
    extension = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    size = models.IntegerField(default=0)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_scanned = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '笔记文件'
        verbose_name_plural = '笔记文件'

    def __str__(self):
        return self.file_path
