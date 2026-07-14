from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('tool/<int:pk>/', views.tool_detail, name='tool_detail'),
    path('tool/<int:pk>/download/', views.tool_download, name='tool_download'),
    path('upload/', views.tool_upload, name='tool_upload'),
]
