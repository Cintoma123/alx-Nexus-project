from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.utils.text import slugify
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with random products and categories"

    def handle(self, *args, **kwargs):
        # Create some categories
        category_data = [
            ("Electronics", "Devices, gadgets, and home electronics."),
            ("Books", "Fiction, non-fiction, and educational books."),
            ("Clothing", "Apparel for men, women, and children."),
            ("Shoes", "Various styles of footwear."),
            ("Accessories", "Watches, bags, jewelry, and more."),
        ]

         categories = []
        for name, desc in category_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                slug=slugify(name),
                defaults={'description': desc}
            )
            # If the category already exists, update description if needed
            if not created:
                cat.description = desc
                cat.save()
            categories.append(cat)
        # Create products
        for _ in range(25):
            name = fake.unique.word().capitalize() + " " + fake.word().capitalize()
            category = random.choice(categories)
            price = round(random.uniform(10.0, 1000.0), 2)
            stock = random.randint(1, 100)
            description = fake.text(max_nb_chars=200)

            Product.objects.create(
                item_name=name,
                price=price,
                slug=slugify(name),
                category=category,
                stock=stock,
                description=description,
                available=random.choice([True, True, False])
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded products and categories!"))
