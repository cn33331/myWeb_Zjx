from django.urls import path
from . import views

urlpatterns = [
    path('tools/', views.ToolListView.as_view(), name='api_tool_list'),
    path('tools/<int:pk>/', views.ToolDetailView.as_view(), name='api_tool_detail'),
    path('tools/<int:pk>/download/', views.ToolDownloadView.as_view(), name='api_tool_download'),
]
