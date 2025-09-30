from django.db import models
from django.contrib.auth.models import User
from orders.models import Order 
from users.models import User
from django.conf import settings
# Create your models here.
class Payment(models.Model):
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , default=1)
    reference = models.CharField(max_length=100, unique=True)  # Paystack reference
    amount = models.DecimalField(max_digits=10, decimal_places=2 , default=1)
    status = models.CharField(max_length=20, default="pending")  # pending, successful, failed
    channel = models.CharField(max_length=50, blank=True, null=True)  # card, bank transfer, ussd
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference} - {self.status}"
