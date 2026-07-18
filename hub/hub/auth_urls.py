from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
