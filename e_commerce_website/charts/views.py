from django.shortcuts import render
from django.http import HttpResponse
from charts.models import Chart, Chartitem
from charts.serializers import ChartSerializer, ChartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from charts.signals import create_user_chart
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChartAPIView(APIView):
    #permission_classes = [IsAuthenticated]  # 
    def get(self, request, format=None):
        serializer = ChartSerializer(request.user.users_chart)
        return Response(serializer.data)
         
                   
class AddChartitemAPIview(APIView):
    def post(self, request, format=None):
        serializer = ChartItemSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
