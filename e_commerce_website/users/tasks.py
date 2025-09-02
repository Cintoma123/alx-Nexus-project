from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user):
    try:
        subject = "welcome cd 🎉 to our e commerce website we are happy to see u"
        message = f"Hi {username},\n\nThanks for registering. We're excited to have you on board!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(
            subject , 
            message , 
            recipient_list,
            fail_silently=False,
            )
        if sent:
            print("Email sent successfully")
        else:
            print("Failed to send email")  
    except Exception as e:
        print(f"An error occurred: {e}")


            

# users/tasks.py

def send_login_email(user):
    try:
        subject = "Login Notification"
        message = f"Hi {user.username}, you just logged in to your account."
        recipient_list = [user.email]
        send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        )
        if sent:
            print("Sending email to:", user.username, user.email)

           

        else:
            print("Failed to send email")
    except Exception as e:
            print(f"An error occurred: {e}")





    

    

    