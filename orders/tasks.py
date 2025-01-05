from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    task to send an e-mail notification when an order is
    successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order no. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed and order.'
        f'Your order Id is {order.id}'
    )
    mail_sent = send_mail(subject, message, 'admin@eshop.com', [order.email])
    return mail_sent

