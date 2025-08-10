from rest_framework import serializers
from products_and_categories.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['item_name', 'price', 'slug', 'category', 'stock', 'description', 'available']

    # checking availability of stock 
    def check_stock(self, validated_data):
        try:
            if 'stock' in validated_data:
                print('the stock is available')
        except KeyError:
            raise serializers.ValidationError("stock is not available")
        return validated_data

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("price must be positive")

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("stock cannot be negative")
