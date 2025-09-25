from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from charts.models import Chart

class Command(BaseCommand):
    help = 'Deletes charts older than one week.'

    def handle(self, *args, **options):
        one_week_ago = timezone.now() - timedelta(weeks=1)
        old_charts = Chart.objects.filter(created_at__lt=one_week_ago)
        count = old_charts.count()
        old_charts.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old charts.'))