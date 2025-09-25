from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from charts.models import Chart
from users.models import User

class Command(BaseCommand):
    help = 'Sends a reminder to users with pending charts.'

    def handle(self, *args, **options):
        three_days_ago = timezone.now() - timedelta(days=3)
        pending_charts = Chart.objects.filter(created_at__lt=three_days_ago)

        for chart in pending_charts:
            if chart.items.exists():
                user = chart.user
                subject = 'You have items in your shopping cart'
                message = f'Dear {user.first_name}, You have items in your shopping cart. Complete your purchase now!'
                send_mail(subject, message, 'admin@myshop.com', [user.email])
                self.stdout.write(self.style.SUCCESS(f'Sent reminder to {user.email}'))