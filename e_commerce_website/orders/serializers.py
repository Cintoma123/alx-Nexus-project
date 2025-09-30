from rest_framework import serializers
from orders.models import Order, OrderItem

class CheckoutSerializer(serializers.Serializer):
    delivery_option = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    note = serializers.CharField(required=False, allow_blank=True)  # optional

    class Meta:
        model = Order 
        fields = ["delivery_option","payment_method","note"]
        read_only_fields = ["note"]

 
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "total_price", "contact_address", "postal_code", "phone_number",
            "delivery_option", "payment_method", "status", "items", "created_at" ,"amount"
        ]
        read_only_fields = fields

    #def create(self, validated_data):
        #items_data = validated_data.pop('items')
       # order = Order.objects.create(**validated_data)
        #for item_data in items_data:
            #OrderItem.objects.create(order=order, **item_data)
        #return order

    