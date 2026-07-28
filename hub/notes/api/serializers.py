from rest_framework import serializers
from ..models import NoteRepository, NoteFile


class NoteRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteRepository
        fields = ['id', 'name', 'repo_type', 'repo_url', 'branch', 'local_path', 'last_sync', 'sync_status', 'sync_message', 'created_at']


class NoteFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteFile
        fields = ['id', 'file_path', 'file_name', 'extension', 'size', 'last_modified', 'last_scanned']


class NoteContentSerializer(serializers.Serializer):
    content = serializers.CharField()
    file_name = serializers.CharField()
    file_path = serializers.CharField()


class SyncResultSerializer(serializers.Serializer):
    repository = serializers.CharField()
    success = serializers.BooleanField()
    message = serializers.CharField()
    notes_count = serializers.IntegerField()


class UploadNoteSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_path = serializers.CharField(required=False, default='')


class DeleteNoteSerializer(serializers.Serializer):
    file_path = serializers.CharField()
