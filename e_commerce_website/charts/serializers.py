from users.models import User
from rest_framework import serializers
from charts.models import Chart, Chartitem
from products_and_categories.serializers import ProductSerializer
from products_and_categories.models import Product


class ChartItemSerializer(serializers.ModelSerializer):
    """Serializer for ChartItem model."""
    product = ProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
        error_messages={
            'does_not_exist': 'Product with id {pk_value} does not exist.'
        }
    )

    class Meta:
        model = Chartitem
        fields = ["id", "chart", "product", "product_id", "quantity", "added_at"]

    def validate_quantity(self, value):
        """Ensure that the quantity is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value


class ChartSerializer(serializers.ModelSerializer):
    """Serializer for Chart model."""
    items =  ChartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Chart
        fields = ["id", "user", "created_at", "items"]
        read_only_fields = ["user"]

    def validate_user(self, value):
        """Ensure that the user exists."""
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value