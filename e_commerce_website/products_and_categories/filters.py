import django_filters
from products_and_categories.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'item_name': ['icontains'],
            'price': ['gte', 'lte'],
             'category': ['exact'],
            'available': ['exact'],
            'slug': ['exact'],
            'description': ['icontains'],
            'stock': ['gte', 'lte'],
            

        }
