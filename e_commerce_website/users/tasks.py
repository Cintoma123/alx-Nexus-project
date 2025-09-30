from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import User

@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        subject = "Welcome to our E-commerce Website! 🎉"
        message = f"Hi {user.username},\n\nThanks for registering. We're excited to have you on board!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        sent_count = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        if sent_count > 0:
            print(f"Welcome email sent successfully to {user.email}")
        else:
            print(f"Failed to send welcome email to {user.email}")
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while sending welcome email: {e}")

@shared_task
def send_login_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        subject = "Login Notification"
        message = f"Hi {user.username},\n\nYou just logged in to your account."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        sent_count = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        if sent_count > 0:
            print(f"Login notification sent successfully to {user.email}")
        else:
            print(f"Failed to send login notification to {user.email}")
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while sending login email: {e}")
