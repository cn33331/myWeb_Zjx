from django.urls import path
from .views import TransferRecordListView, TransferRecordDetailView

urlpatterns = [
    path('records/', TransferRecordListView.as_view(), name='transfer-record-list'),
    path('records/<int:pk>/', TransferRecordDetailView.as_view(), name='transfer-record-detail'),
]
