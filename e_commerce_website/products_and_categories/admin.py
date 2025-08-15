from django.contrib import admin
# Register your models here.
from products_and_categories.models import Product, Category

admin.site.register(Category)
admin.site.register(Product)

