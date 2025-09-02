from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from users.models import User, Profile
from charts.models import Chart
from users.tasks import send_welcome_email , send_login_email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # only run when user is first created
        Profile.objects.create(user=instance)

 
    