from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.permissions import AllowAny , IsAuthenticated
from orders.serializers import OrderSerializer , OrderItemSerializer, CheckoutSerializer
from orders.models import Order , OrderItem
from charts.models import Chartitem , Chart
from users.models import User ,Profile
from orders.middleware import BlockWeekendOrdersMiddleware
from orders.tasks import order_created
class CheckoutViewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=400)

        cart_items = Chartitem.objects.filter(chart__user=request.user)
        if not cart_items.exists():
            return Response({"error": "Chart is empty"}, status=400)

        total_price = sum([item.product.price * item.quantity for item in cart_items])

        order = Order.objects.create(
            user=request.user,
            email=user.email,
            contact_address=profile.contact_address,
            postal_code=profile.postal_code,
            phone_number=profile.phone_number,
            total_price=total_price
        )
        order_created.delay(user.email)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        #cart_items.delete()
        return Response(OrderSerializer(order).data, status=200)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.get(user=request.user)
        status = request.data.get("status")

        if status in ["processing", "shipped", "delivered"]:
            order.status = status
            order.save()
            return Response({"message": f"Order status updated to {status}"})
        return Response({"error": "Invalid status"}, status=400)
