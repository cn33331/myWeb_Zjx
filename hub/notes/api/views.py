import os
from pathlib import Path
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import NoteRepository, NoteFile
from ..git_service import sync_notes, get_note_content, GitService, build_file_tree, parse_toc
from .serializers import (
    NoteRepositorySerializer,
    NoteFileSerializer,
    NoteContentSerializer,
    SyncResultSerializer,
    UploadNoteSerializer,
    DeleteNoteSerializer
)


class NoteRepositoryList(generics.ListCreateAPIView):
    queryset = NoteRepository.objects.all()
    serializer_class = NoteRepositorySerializer
    permission_classes = [AllowAny]


class NoteRepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NoteRepository.objects.all()
    serializer_class = NoteRepositorySerializer
    permission_classes = [AllowAny]


class NoteFileList(generics.ListAPIView):
    serializer_class = NoteFileSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        repository_id = self.kwargs.get('repository_id')
        queryset = NoteFile.objects.filter(repository_id=repository_id)
        
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(file_name__icontains=search) | queryset.filter(file_path__icontains=search)
        
        return queryset.order_by('-last_modified')


class NoteContentDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        file_path = kwargs.get('file_path')
        
        content = get_note_content(file_path, repository_id)
        
        if content is None:
            return Response(
                {'error': '笔记文件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            note_file = NoteFile.objects.get(file_path=file_path, repository_id=repository_id)
            data = {
                'content': content,
                'file_name': note_file.file_name,
                'file_path': note_file.file_path
            }
        except NoteFile.DoesNotExist:
            data = {
                'content': content,
                'file_name': file_path.split('/')[-1],
                'file_path': file_path
            }
        
        return Response(data)


class SyncNotesView(generics.GenericAPIView):
    serializer_class = SyncResultSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        results = sync_notes(repository_id)
        
        if not results:
            return Response(
                {'error': '未找到仓库'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(results)


class QuickSyncView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        repo_url = request.data.get('repo_url', '')
        local_path = request.data.get('local_path', '')
        
        if not repo_url or not local_path:
            return Response(
                {'error': '缺少必要参数 repo_url 或 local_path'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        repo, created = NoteRepository.objects.get_or_create(
            repo_url=repo_url,
            defaults={
                'name': repo_url.split('/')[-1].replace('.git', ''),
                'local_path': local_path
            }
        )
        
        if not created:
            repo.local_path = local_path
            repo.save()
        
        service = GitService(repo)
        result = service.sync_and_scan()
        
        return Response({
            'success': result['success'],
            'message': result.get('sync_message', result.get('stderr', '')),
            'notes_count': result.get('notes_count', 0),
            'repository_id': repo.id
        })


class FileTreeView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        tree = build_file_tree(repository_id)
        return Response(tree)


class NoteDetailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        file_path = kwargs.get('file_path')
        
        content = get_note_content(file_path, repository_id)
        
        if content is None:
            return Response(
                {'error': '笔记文件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        toc = parse_toc(content)
        
        try:
            note_file = NoteFile.objects.get(file_path=file_path, repository_id=repository_id)
            data = {
                'content': content,
                'file_name': note_file.file_name,
                'file_path': note_file.file_path,
                'size': note_file.size,
                'last_modified': note_file.last_modified,
                'toc': toc
            }
        except NoteFile.DoesNotExist:
            data = {
                'content': content,
                'file_name': file_path.split('/')[-1],
                'file_path': file_path,
                'toc': toc
            }
        
        return Response(data)


class UploadNoteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadNoteSerializer

    def post(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        
        try:
            repo = NoteRepository.objects.get(id=repository_id)
        except NoteRepository.DoesNotExist:
            return Response({'error': '仓库不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if repo.repo_type != 'local':
            return Response({'error': '只能上传到本地仓库'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': '未提供文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = request.data.get('file_path', '')
        file_name = uploaded_file.name
        extension = os.path.splitext(file_name)[1]
        
        content = uploaded_file.read().decode('utf-8', errors='ignore')
        
        if file_path:
            full_path = os.path.join(repo.local_path, file_path)
        else:
            full_path = os.path.join(repo.local_path, file_name)
            file_path = file_name
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        size = os.path.getsize(full_path)
        
        note_file, created = NoteFile.objects.update_or_create(
            repository=repo,
            file_path=file_path,
            defaults={
                'file_name': file_name,
                'extension': extension,
                'content': content,
                'size': size,
                'last_modified': timezone.now(),
                'last_scanned': timezone.now()
            }
        )
        
        return Response({
            'success': True,
            'file_path': file_path,
            'file_name': file_name,
            'size': size,
            'created': created
        })


class DeleteNoteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteNoteSerializer

    def post(self, request, *args, **kwargs):
        repository_id = kwargs.get('repository_id')
        
        try:
            repo = NoteRepository.objects.get(id=repository_id)
        except NoteRepository.DoesNotExist:
            return Response({'error': '仓库不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if repo.repo_type != 'local':
            return Response({'error': '只能删除本地仓库的文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = request.data.get('file_path', '')
        if not file_path:
            return Response({'error': '未提供文件路径'}, status=status.HTTP_400_BAD_REQUEST)
        
        full_path = os.path.join(repo.local_path, file_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
        
        NoteFile.objects.filter(
            repository=repo,
            file_path=file_path
        ).delete()
        
        return Response({
            'success': True,
            'file_path': file_path
        })


class InitializeLocalRepoView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        local_path = request.data.get('local_path', '/tmp/local-notes')
        
        repo, created = NoteRepository.objects.get_or_create(
            repo_type='local',
            defaults={
                'name': '本地笔记仓库',
                'local_path': local_path,
                'sync_status': 'synced'
            }
        )
        
        if not created:
            repo.local_path = local_path
            repo.save()
        
        os.makedirs(local_path, exist_ok=True)
        
        return Response({
            'success': True,
            'repository_id': repo.id,
            'created': created,
            'local_path': local_path
        })
