# tasks.py
import africastalking
from django.conf import settings

from .models import Order


def send_order_confirmation_sms(order_id):
    order = Order.objects.get(id=order_id)
    # customer_phone = str(order.buyer.phone_number)
    customer_phone = "+254798556797"

    africastalking.initialize(
        settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
    ),
    sms = africastalking.SMS

    message = f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: {order.total_cost}."

    def on_finish(error, response):
        if error is not None:
            raise error

    sms.send(message, [customer_phone], callback=on_finish)
