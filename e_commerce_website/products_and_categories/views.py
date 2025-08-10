from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from products_and_categories.serializers import CategorySerializer , ProductSerializer
from products_and_categories.models import Product , Category
from products_and_categories.filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404

# Create your views here.


class CategoryListAPIview(APIView):
    permission_classes = [AllowAny]
    def get (self , request , format=None):
        query_set = Category.objects.all()
        serializer = CategorySerializer(query_set , many=True)
        return Response(
    {
        "message": "Categories displayed successfully.",
        "data": serializer.data
    },
    status=status.HTTP_200_OK
)

class CategorydetailsAPIview(APIView):
    permission_classes = [AllowAny]
    def get(self , request ,pk):
        categorys = get_object_or_404(Category , pk=pk)
        serializer = CategorySerializer(categorys)
        return Response(serializers.data,status=status.HTTP_200_OK)


class ProductpaginateAPIview(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        print("products counted successfully.")
        return super().list(request, *args, **kwargs)


class ProductListAPIview(ListAPIView):
    permission_classes = [AllowAny]
    def get (self , request , format=None):
        query_set = Product.objects.all()
        serializer = ProductSerializer(query_set , many=True)
        return Response(
    {
        "message": "products displayed successfully.",
        "data": serializer.data
    },
    status=status.HTTP_200_OK
)
 

 
class ProductfiltersearchAPIview(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    #filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
        
class ProductdetailsAPIview(APIView):
    permission_classes = [AllowAny]
    def get(self , request ,pk):
        products = get_object_or_404(Product , pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializers.data,status=status.HTTP_200_OK)
