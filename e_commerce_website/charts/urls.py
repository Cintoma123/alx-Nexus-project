from django.contrib import admin
from django.urls import path
from charts.views import (
    AddChartitemAPIview,
    ChartAPIView,
    RemoveChartitemAPIview,
)

urlpatterns = [
    path('add-chart/', AddChartitemAPIview.as_view(), name='add-chart'),
    path('charts/', ChartAPIView.as_view(), name='charts'),
    path('remove-chart-item/<int:item_id>/', RemoveChartitemAPIview.as_view(), name='remove-chart-item'),
]