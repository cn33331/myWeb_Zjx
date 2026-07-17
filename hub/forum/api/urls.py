from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.TopicListView.as_view(), name='api_topic_list'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='api_topic_detail'),
    path('topics/<int:topic_pk>/posts/', views.PostListView.as_view(), name='api_post_list'),
]
