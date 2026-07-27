from django.apps import AppConfig
import os


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

    def ready(self):
        self.init_local_repo()

    def init_local_repo(self):
        try:
            from .models import NoteRepository
            
            local_path = '/tmp/local-notes'
            os.makedirs(local_path, exist_ok=True)
            
            repo, created = NoteRepository.objects.get_or_create(
                repo_type='local',
                defaults={
                    'name': '本地笔记仓库',
                    'local_path': local_path,
                    'sync_status': 'synced'
                }
            )
            
            if created:
                print(f'[Notes] 本地仓库已创建: {local_path} (ID: {repo.id})')
            else:
                if repo.local_path != local_path:
                    repo.local_path = local_path
                    repo.save()
        except Exception as e:
            print(f'[Notes] 初始化本地仓库失败: {e}')
