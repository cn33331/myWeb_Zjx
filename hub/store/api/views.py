from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import FileResponse
from store.models import Tool
from .serializers import ToolSerializer


class ToolListView(generics.ListCreateAPIView):
    queryset = Tool.objects.all().order_by('-upload_date')
    serializer_class = ToolSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save()


class ToolDetailView(generics.RetrieveDestroyAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [permissions.AllowAny]


class ToolDownloadView(generics.GenericAPIView):
    queryset = Tool.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        tool = self.get_object()
        tool.downloads += 1
        tool.save()
        return FileResponse(tool.file.open(), as_attachment=True)
