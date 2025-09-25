from django.urls import path
from orders.views import OrderCreateAPIView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order_create'),
]