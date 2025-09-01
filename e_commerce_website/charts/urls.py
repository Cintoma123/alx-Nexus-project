from django.contrib import admin
from django.urls import path
from charts.views import (
    AddChartitemAPIview,
    ChartAPIView,


)
urlpatterns = [
    path('add-chart/',AddChartitemAPIview.as_view(), name='add-chart'),
    path('charts/',ChartAPIView.as_view(), name='charts'),
    
]
