from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name}, You have successfully placed an order. Your order ID is {order.id}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        mail_sent = send_mail(subject,
                          message,
                          from_email,
                          recipient_list,
                          fail_silently = False,
        )
        if sent_count > 0:
            print(f"order_created message sent successfully to {user.email}")
        else:
            print(f"Failed to send order_created email to {user.email}")
    except Order.DoesNotExist:
        print(f"order_id with id {order_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while sending welcome email: {e}")

        


 