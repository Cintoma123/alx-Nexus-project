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
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    def get(self , request ,slug):
        categorys = get_object_or_404(Category , slug=slug)
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
class ProductcreateAPIview(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated or not request.user.is_staff:
                return Response(
                    {"message": "You are not authorized to create a product."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except NameError:
            return Response(
                {"message": "Admin user is not defined."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = ProductSerializer(data=request.data)
        # Check if the serializer is valid
        if serializer.is_valid():
           serializer.save()
           return Response(
                {
                    "message": "Product created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Product creation failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
class ProductupdateAPIview(APIView):
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    def put(self, request, slug, *args, **kwargs):
        try:
            if not request.user.is_authenticated or not request.user.is_staff:
                return Response(
                    {"message": "You are not authorized to update this product."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except NameError:
            return Response(
                {"message": "User is not defined."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # Assuming 'slug' is a unique identifier for the product
        # If you are using 'pk' instead, change the get_object_or_404 line
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Product update failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductdeleteAPIview(APIView):
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    def delete(self, request, slug, *args, **kwargs):
        try:
            if not request.user.is_authenticated or not request.user.is_staff:
                return Response(
                    {"message": "You are not authorized to delete this product."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except NameError:
            return Response(
                {"message": "User is not defined."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        product = get_object_or_404(Product, slug=slug)
        product.delete()
        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
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
