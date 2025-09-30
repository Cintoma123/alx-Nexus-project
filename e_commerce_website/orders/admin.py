from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "total_price",
        "payment_method",
        "status",          
        "created_at",    
        "updated_at",  
    ]
    list_filter = ["status", "created_at", "updated_at"]  
    search_fields = [ "paystack_reference"]
    ordering = ["-created_at"]  
