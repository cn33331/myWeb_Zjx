from rest_framework import serializers
from transfer.models import TransferRecord


class TransferRecordSerializer(serializers.ModelSerializer):
    platform_name = serializers.SerializerMethodField()

    class Meta:
        model = TransferRecord
        fields = ['id', 'platform', 'platform_name', 'code', 'link', 'file_name', 'file_size', 'notes', 'created_at']

    def get_platform_name(self, obj):
        return obj.get_platform_display()
