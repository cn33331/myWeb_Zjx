from rest_framework import generics, permissions
from transfer.models import TransferRecord
from .serializers import TransferRecordSerializer


class TransferRecordListView(generics.ListCreateAPIView):
    queryset = TransferRecord.objects.all().order_by('-created_at')
    serializer_class = TransferRecordSerializer
    permission_classes = [permissions.AllowAny]


class TransferRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRecord.objects.all()
    serializer_class = TransferRecordSerializer
    permission_classes = [permissions.AllowAny]
