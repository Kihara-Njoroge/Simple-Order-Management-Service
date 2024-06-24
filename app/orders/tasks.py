# tasks.py
import africastalking
from decouple import config

username = config("AFRICASTALKING_USERNAME")
api_key = config("AFRICASTALKING_API_KEY")


def send_order_confirmation_sms(order):
    customer_phone = str(order.buyer.phone_number)
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    message = f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: KES {order.total_cost}."

    def on_finish(error, response):
        if error is not None:
            raise error

    sms.send(message, [customer_phone], callback=on_finish)
