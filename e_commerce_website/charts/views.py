from charts.serializers import ChartSerializer, ChartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from charts.models import Chartitem , Chart
from products_and_categories.models import Product
from django.shortcuts import get_object_or_404



class ChartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        chart , created = Chart.objects.get_or_create(user=request.user)
        serializer = ChartSerializer(chart)
        return Response(serializer.data)


class AddChartitemAPIview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        chart, created = Chart.objects.get_or_create(user=request.user)
         
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": f"Product with id {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(quantity, int) or quantity <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock < quantity:
            return Response({"error": "Requested quantity exceeds stock."}, status=status.HTTP_400_BAD_REQUEST)

        chart_item, created =  Chartitem.objects.get_or_create(
            chart=chart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            chart_item.quantity += quantity
            chart_item.save()
        
        serializer = ChartItemSerializer(chart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveChartitemAPIview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id, format=None):
        try:
            chart_item = Chartitem.objects.get(id=item_id)
        except Chartitem.DoesNotExist:
            return Response({"error": "Chart item not found."}, status=status.HTTP_404_NOT_FOUND)

        if chart_item.chart != request.user.users_chart:
            return Response({"error": "You do not have permission to delete this item."}, status=status.HTTP_403_FORBIDDEN)

        chart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)