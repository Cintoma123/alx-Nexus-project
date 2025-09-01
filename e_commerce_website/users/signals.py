from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Profile
from charts.models import Chart

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # only run when user is first created
        Profile.objects.create(user=instance)
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
    #"""Ensure profile is saved when user is saved."""
    #instance.Profile.save()