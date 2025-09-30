from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.permissions import AllowAny , IsAuthenticated
from users.serializers import RegistrationSerializer, LoginSerializer , ChangepasswordSerializer , ProfileSerializer, LogoutSerializer
from users.tasks import send_welcome_email, send_login_email
from users.models import User , Profile
from rest_framework.decorators import action
from users.utils import get_tokens_for_user
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_description="change password",
        responses={200: ChangepasswordSerializer(many=True)}
    )


    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
          user =  serializer.save()
          send_welcome_email.delay(user.id)
          return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="login user",
        responses={200: LoginSerializer(many=True)}
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email ,password=password)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user is not None:
            send_login_email.delay(user.id)
            tokens = get_tokens_for_user(user)
            return Response({
            "token": tokens,
            "message": "Login successful",
            "user": serializer.validated_data
        }, status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'} ,status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get all listings",
        responses={200: ChangepasswordSerializer(many=True)}
    )

    def post(self, request):
        serializer = ChangepasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            if not request.data.get("refresh"):
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)