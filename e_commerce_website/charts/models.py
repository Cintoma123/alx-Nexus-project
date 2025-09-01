from django.db import models
from rest_framework import serializers
from users.models import User
from products_and_categories.models import Product
from products_and_categories.serializers import Product
# Create your models here.
class Chart(models.Model):
    """Model representing a chart in the e-commerce website."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_chart')
    created_at = models.DateTimeField(auto_now_add=True)
    #items = models.ForeignKey('Chartitem', on_delete=models.CASCADE, related_name='items_chart', blank=True)
    #name = models.CharField(max_length=100, default="My Cart")
    class Meta:
        verbose_name = "chart"
        verbose_name_plural = "charts"

    def __str__(self):
        return self.user

    #def save(self, *args, **kwargs):
        #"""Override save method to ensure unique chart names."""
        #if not self.name:
            #raise ValueError("Chart name cannot be empty.")
        #super().save(*args, **kwargs)

class Chartitem(models.Model):
    """Model representing an item in a chart."""
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_item')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    #product_id = serializers.PrimaryKeyRelatedField(
        #queryset=Product.objects.all(), source="product", write_only=True
    #)

    #product_id = models.IntegerField()


    def __str__(self):
        return self.chart
        