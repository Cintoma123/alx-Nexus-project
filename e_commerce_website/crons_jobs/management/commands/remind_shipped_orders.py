from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from orders.models import Order

class Command(BaseCommand):
    help = 'Sends a reminder to users for orders that have not been shipped for 5 days after payment.'

    def handle(self, *args, **options):
        five_days_ago = timezone.now() - timedelta(days=5)
        unshipped_orders = Order.objects.filter(
            paid=True, 
            shipped=False, 
            updated__lt=five_days_ago
        )

        for order in unshipped_orders:
            user = order.email
            subject = 'Your order has been shipped!'
            message = f'Dear {order.first_name}, Your order with ID {order.id} has been shipped.'
            send_mail(subject, message, 'admin@myshop.com', [user])
            order.shipped = True
            order.save()
            self.stdout.write(self.style.SUCCESS(f'Sent shipping confirmation for order {order.id}'))