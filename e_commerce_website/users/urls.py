from django.contrib import admin
from django.urls import path
from users.views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    ChangePasswordAPIView,
    UserProfileAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
