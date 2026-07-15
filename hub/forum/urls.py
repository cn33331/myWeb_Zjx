from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('login/', views.forum_login, name='forum_login'),
    path('logout/', views.forum_logout, name='forum_logout'),
    path('register/', views.forum_register, name='forum_register'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/new/', views.create_topic, name='create_topic'),
    path('admin/review/', views.admin_review, name='admin_review'),
]