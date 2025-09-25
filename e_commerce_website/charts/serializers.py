from users.models import User
from rest_framework import serializers
from charts.models import Chart, Chartitem
from products_and_categories.serializers import ProductSerializer
from products_and_categories.models import Product


class ChartItemSerializer(serializers.ModelSerializer):
    """Serializer for ChartItem model."""
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source="product.item_name", read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Chartitem
        fields = ["id", "chart", "product", "product_name", "product_id", "quantity", "added_at"]
        read_only_fields = ["chart"]

    def create(self, validated_data):
        chart = self.context['request'].user.users_chart
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")

        chart_item, created = Chartitem.objects.get_or_create(
            chart=chart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            chart_item.quantity += quantity
            chart_item.save()
        return chart_item

    def validate_product(self, value):
        """Ensure that the product exists."""
        if not value:
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        if product and quantity and product.stock < quantity:
            raise serializers.ValidationError("Requested quantity exceeds stock.")
        return attrs

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

    







