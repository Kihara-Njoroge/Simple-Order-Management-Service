import logging
import smtplib

import africastalking
from decouple import config
from django.conf import settings

LOGGER = logging.getLogger(__name__)

username = config("AFRICASTALKING_USERNAME")
api_key = config("AFRICASTALKING_API_KEY")


def send_order_confirmation_sms(order):
    customer_phone = str(order.buyer.phone_number) if order.buyer.phone_number else None

    if customer_phone:
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS

        message = f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: KES {order.total_cost}."

        def on_finish(error, response):
            if error is not None:
                raise error

        sms.send(message, [customer_phone], callback=on_finish)
    else:
        subject = "Order Confirmation"
        message = f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: KES {order.total_cost}."
        from_email = settings.DEFAULT_FROM_EMAIL
        body = f"Subject: {subject}\n\n{message}"
        recipient_list = [order.buyer.email]

        try:
            # For SSL connection (port 465)
            server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
            server.login(from_email, settings.EMAIL_HOST_PASSWORD)

            for email in recipient_list:
                server.sendmail(settings.DEFAULT_FROM_EMAIL, email, body)

            server.quit()
        except Exception as e:
            LOGGER.error(f"Failed to order confirmation email: {e}")
