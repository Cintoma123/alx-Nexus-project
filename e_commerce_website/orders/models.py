from django.db import models
from products_and_categories.models import Product
from users.models import User


class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    DELIVERY_CHOICES = [
        ("home_delivery", "Home Delivery"),
        ("pickup", "Pickup at Store"),
    ]

    PAYMENT_CHOICES = [
        ("paystack", "Paystack"),
        ("cash_on_delivery", "Cash on Delivery"),
        ("bank_transfer", "Bank Transfer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', default=1)
    first_name =  models.CharField(max_length=255, null=True, blank=True)
    last_name =  models.CharField(max_length=255, null=True, blank=True)
    contact_address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2 , default=1)
    postal_code =  models.CharField(max_length=255, null=True, blank=True)
    phone_number =  models.CharField(max_length=255, null=True, blank=True)
    delivery_option = models.CharField(max_length=20, null=True, choices=DELIVERY_CHOICES)
    payment_method = models.CharField(max_length=20, null=True, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # pending/paid/shipped
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity