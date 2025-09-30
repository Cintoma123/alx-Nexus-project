from django.urls import path
from orders.views import CheckoutViewAPIView  , UpdateOrderStatusView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('check_out/', CheckoutViewAPIView.as_view(), name = "check_out"),
    path('update_order/', UpdateOrderStatusView.as_view(), name = "update_order")
]