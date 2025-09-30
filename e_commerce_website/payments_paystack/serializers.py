from rest_framework import serializers
from payments_paystack.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "order", "reference", "amount", "status", "channel", "created_at"]
        read_only_fields = ["id", "order", "reference","status", "channel","created_at"]
