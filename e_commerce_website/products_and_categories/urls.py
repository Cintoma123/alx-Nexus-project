from django.contrib import admin
from django.urls import path
from products_and_categories.views import (
    CategoryListAPIview,
    CategorydetailsAPIview,
    ProductListAPIview,
    ProductfiltersearchAPIview,
    ProductdetailsAPIview,
    ProductpaginateAPIview,
)

urlpatterns = [
    path('category-list/',CategoryListAPIview.as_view(), name='category-list'),
    path('category-details/<int:pk>/', CategorydetailsAPIview.as_view(), name='category-details'),
    path('product-list/', ProductListAPIview.as_view(), name='product-list'),
    path('product-search/', ProductfiltersearchAPIview.as_view(), name='product-search'),
    path('product-details/<int:pk>/',  ProductdetailsAPIview.as_view(), name='product-details'),
    path('product-paginate/', ProductpaginateAPIview.as_view(), name='product-paginate'),
]
