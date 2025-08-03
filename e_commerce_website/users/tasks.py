from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_mail(username , email):
    subject = "welcome to our e commerce website we are happy to see u"
    message = f"Hi {username},\n\nThanks for registering. We're excited to have you on board!"
    from_email = 'no-reply@yourdomain.com'
    send_mail(subject , message , from_email , [email], fail_sliently=False)