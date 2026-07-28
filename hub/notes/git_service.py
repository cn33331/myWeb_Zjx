import os
import subprocess
import shutil
import logging
from datetime import datetime
from pathlib import Path
from django.utils import timezone

from .models import NoteRepository, NoteFile

logger = logging.getLogger(__name__)


class GitService:
    def __init__(self, repository):
        self.repository = repository
        self.repo_url = repository.repo_url
        self.local_path = Path(repository.local_path)
        self.branch = repository.branch or 'main'

    def _run_git_command(self, command, cwd=None):
        try:
            logger.info(f'Running git command: {" ".join(command)}')
            result = subprocess.run(
                command,
                cwd=cwd or str(self.local_path),
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                logger.error(f'Git command failed: {result.stderr}')
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            logger.error('Git command timed out')
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out'
            }
        except Exception as e:
            logger.exception(f'Git command error: {e}')
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e)
            }

    def clone_repository(self):
        if self.local_path.exists():
            shutil.rmtree(str(self.local_path))
        
        command = ['git', 'clone', '--branch', self.branch, self.repo_url, str(self.local_path.name)]
        result = self._run_git_command(command, cwd=str(self.local_path.parent))
        
        if result['success']:
            self.repository.sync_status = 'synced'
            self.repository.sync_message = f'克隆成功 (分支: {self.branch})'
            self.repository.last_sync = timezone.now()
            self.repository.save()
        else:
            self.repository.sync_status = 'failed'
            self.repository.sync_message = result['stderr'] or '克隆失败'
            self.repository.save()
        
        return result

    def pull_latest(self):
        if not self.local_path.exists():
            return self.clone_repository()
        
        # 确保在正确的分支上
        current_branch_result = self._run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        current_branch = current_branch_result['stdout'] if current_branch_result['success'] else ''
        
        if current_branch and current_branch != self.branch:
            # 切换分支
            self._run_git_command(['git', 'checkout', self.branch])
        
        # 先尝试 fetch
        fetch_result = self._run_git_command(['git', 'fetch', 'origin'])
        
        # 使用 --rebase 拉取，避免分支分歧问题
        pull_result = self._run_git_command(['git', 'pull', '--rebase', 'origin', self.branch])
        
        if not pull_result['success']:
            # 如果 rebase 失败，尝试放弃本地更改后重置
            reset_result = self._run_git_command(['git', 'reset', '--hard', f'origin/{self.branch}'])
            if reset_result['success']:
                pull_result = {
                    'success': True,
                    'stdout': f'已重置到 origin/{self.branch}',
                    'stderr': ''
                }
        
        if not pull_result['success']:
            # 最后手段：删除仓库重新克隆
            import shutil
            if self.local_path.exists():
                shutil.rmtree(str(self.local_path))
            return self.clone_repository()
        
        if pull_result['success']:
            self.repository.sync_status = 'synced'
            self.repository.sync_message = pull_result['stdout'] or f'拉取成功 (分支: {self.branch})'
            self.repository.last_sync = timezone.now()
            self.repository.save()
        else:
            self.repository.sync_status = 'failed'
            self.repository.sync_message = pull_result['stderr'] or '拉取失败'
            self.repository.save()
        
        return pull_result

    def get_branches(self):
        result = self._run_git_command(['git', 'ls-remote', '--heads', self.repo_url])
        
        if not result['success']:
            result = self._run_git_command(['git', 'ls-remote', self.repo_url])
        
        branches = []
        if result['success']:
            for line in result['stdout'].split('\n'):
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        ref = parts[1]
                        if ref.startswith('refs/heads/'):
                            branch_name = ref.replace('refs/heads/', '')
                            branches.append(branch_name)
        
        if not branches:
            branches = ['main', 'master']
        
        return {
            'success': result['success'],
            'branches': branches,
            'message': result['stderr'] if not result['success'] else None
        }

    def get_git_status(self):
        result = self._run_git_command(['git', 'log', '--oneline', '-1'])
        if result['success']:
            return result['stdout']
        return '未知状态'

    def scan_notes(self):
        NoteFile.objects.filter(repository=self.repository).delete()
        
        note_files = []
        for root, dirs, files in os.walk(self.local_path):
            dirs[:] = [d for d in dirs if d not in ('.git', '.obsidian', '__pycache__')]
            
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.local_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        content = ''
                    
                    file_stat = os.stat(file_path)
                    last_modified = datetime.fromtimestamp(file_stat.st_mtime)
                    last_modified = timezone.make_aware(last_modified)
                    
                    note_file = NoteFile(
                        repository=self.repository,
                        file_path=str(rel_path),
                        file_name=file,
                        extension='.md',
                        content=content,
                        size=file_stat.st_size,
                        last_modified=last_modified,
                        last_scanned=timezone.now()
                    )
                    note_files.append(note_file)
        
        NoteFile.objects.bulk_create(note_files)
        return len(note_files)

    def sync_and_scan(self):
        pull_result = self.pull_latest()
        if pull_result['success']:
            count = self.scan_notes()
            pull_result['notes_count'] = count
        return pull_result


def sync_notes(repository_id=None):
    if repository_id:
        repositories = NoteRepository.objects.filter(id=repository_id)
    else:
        repositories = NoteRepository.objects.all()
    
    results = []
    for repo in repositories:
        service = GitService(repo)
        result = service.sync_and_scan()
        results.append({
            'repository': repo.name,
            'success': result['success'],
            'message': repo.sync_message or result.get('stderr', ''),
            'notes_count': result.get('notes_count', 0)
        })
    return results


def get_note_content(file_path, repository_id):
    try:
        note_file = NoteFile.objects.get(file_path=file_path, repository_id=repository_id)
        return note_file.content
    except NoteFile.DoesNotExist:
        return None


def build_file_tree(repository_id):
    notes = NoteFile.objects.filter(repository_id=repository_id).order_by('file_path')
    
    tree = []
    for note in notes:
        parts = note.file_path.split('/')
        current_level = tree
        
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                exists = False
                for item in current_level:
                    if item['name'] == part and item.get('is_file'):
                        exists = True
                        break
                if not exists:
                    current_level.append({
                        'name': part,
                        'file_path': note.file_path,
                        'file_name': note.file_name,
                        'size': note.size,
                        'last_modified': note.last_modified,
                        'is_file': True,
                        'children': []
                    })
            else:
                found = False
                for item in current_level:
                    if item['name'] == part and not item.get('is_file'):
                        current_level = item['children']
                        found = True
                        break
                if not found:
                    new_dir = {
                        'name': part,
                        'is_file': False,
                        'children': []
                    }
                    current_level.append(new_dir)
                    current_level = new_dir['children']
    
    return tree


def parse_toc(content):
    import re
    
    toc = []
    lines = content.split('\n')
    
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            
            slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '-', title.lower()).strip('-')
            if not slug:
                slug = f'heading-{len(toc)}'
            
            toc.append({
                'level': level,
                'title': title,
                'slug': slug
            })
    
    return toc
