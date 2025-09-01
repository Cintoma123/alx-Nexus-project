from users.models import User
from rest_framework import serializers
from charts.models import Chart, Chartitem
#from charts.serializers import ChartSerializer, ChartItemSerializer
from products_and_categories.serializers import CategorySerializer , ProductSerializer
from products_and_categories.models import Product , Category



class ChartItemSerializer(serializers.ModelSerializer):
    """Serializer for ChartItem model."""
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source="product.item_name", read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Chartitem
        fields = ["id", "chart", "product", "product_name", "product_id" , "quantity", "added_at"]

    def create(self, validated_data):
        chart = validated_data.get("chart")
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        #product_id = validated_data.get("product_id")

        #if chart is None:
           #user = validated_data.get("user")  # you must pass user id in request
           #chart, _ = Chart.objects.get_or_create(user=user)

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

    def validate_chart(self, value):
        """Ensure that the chart exists."""
        if not Chart.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Chart does not exist.")
        return value


class ChartSerializer(serializers.ModelSerializer):
    """Serializer for Chart model."""
    #items =  ChartItemSerializer(many=True, read_only=True)  # nested relationship
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_chart')

    class Meta:
        model = Chart
        fields = ["id", "user", "created_at"]
        #read_only_fields = ["user"]

    def validate_user(self, value):
        """Ensure that the user exists."""
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    def create(self , validated_data):
        validated_data["user"] = self.context["request"].user
        return
        super().create(validated_data)

    







