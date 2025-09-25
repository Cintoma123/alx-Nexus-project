from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from users.models import User

class Command(BaseCommand):
    help = 'Sends a reminder to users to update their profile 48 hours after registration.'

    def handle(self, *args, **options):
        two_days_ago = timezone.now() - timedelta(days=2)
        new_users = User.objects.filter(date_joined__lt=two_days_ago)

        for user in new_users:
            if not hasattr(user, 'profile') or not user.profile.phone_number:
                subject = 'Update your profile'
                message = f'Dear {user.username}, Please update your profile to enjoy all the features of our website.'
                send_mail(subject, message, 'admin@myshop.com', [user.email])
                self.stdout.write(self.style.SUCCESS(f'Sent reminder to {user.email}'))