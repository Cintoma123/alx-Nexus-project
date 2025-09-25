from django.db import models
from users.models import User
from products_and_categories.models import Product

# Create your models here.
class Chart(models.Model):
    """Model representing a chart in the e-commerce website."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_chart')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "chart"
        verbose_name_plural = "charts"

    def __str__(self):
        return f"{self.user.username}'s Cart"

class Chartitem(models.Model):
    """Model representing an item in a chart."""
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_item')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.item_name}"
        