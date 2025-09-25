from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from orders.tasks import order_created

class OrderCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order_created.delay(order.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)