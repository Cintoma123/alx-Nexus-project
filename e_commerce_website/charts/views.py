from charts.serializers import ChartSerializer, ChartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class ChartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = ChartSerializer(request.user.users_chart)
        return Response(serializer.data)


class AddChartitemAPIview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
