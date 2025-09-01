from django.contrib import admin
from django.urls import path
from users.views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    ChangePasswordAPIView,
    UserProfileAPIView,
    UserLoginoutAPIView
)
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('logout/', UserLoginoutAPIView.as_view(), name='logout'),
    #path("api/users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    #path("api/users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
