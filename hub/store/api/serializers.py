from rest_framework import serializers
from store.models import Tool


class ToolSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'version', 'downloads', 'upload_date', 'download_url', 'file']

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/store/tools/{obj.id}/download/')
