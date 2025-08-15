from django.db import models
#import uuid
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = "category"
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name

class Product(models.Model):
    """Model representing a product in the e-commerce website."""
    #
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    #image = models.ImageField(upload_to='products/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.item_name)
        super().save(*args, **kwargs)


    
    def __str__(self):
        return self.item_name
