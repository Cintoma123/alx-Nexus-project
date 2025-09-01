# charts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from charts.models import Chart

@receiver(post_save, sender=User)
def create_user_chart(sender, instance, created, **kwargs):
    if created:  # only run when user is first created
        Chart.objects.create(user=instance)
