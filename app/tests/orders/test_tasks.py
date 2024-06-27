# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# import smtplib
# from django.conf import settings
# from app.orders.tasks import send_order_confirmation_sms

# class Order:
#     def __init__(self, order_no, total_cost, buyer):
#         self.order_no = order_no
#         self.total_cost = total_cost
#         self.buyer = buyer

# class Buyer:
#     def __init__(self, phone_number, email):
#         self.phone_number = phone_number
#         self.email = email

# class SendOrderConfirmationSMSTest(TestCase):
#     @patch("app.orders.tasks.africastalking.SMS.send")
#     @patch("app.orders.tasks.africastalking.initialize")
#     @patch("app.orders.tasks.config")
#     def test_send_order_confirmation_sms(self, mock_config, mock_initialize, mock_send):
#         # Mocking the config values for africastalking
#         mock_config.side_effect = lambda key: {
#             "AFRICASTALKING_USERNAME": "mock_username",
#             "AFRICASTALKING_API_KEY": "mock_api_key"
#         }[key]

#         # Test case where phone number is available
#         buyer = Buyer(phone_number="+254712345678", email="buyer@example.com")
#         order = Order(order_no="e245dae4-147a-4743-bc3a-597b5e369318", total_cost=1000, buyer=buyer)

#         send_order_confirmation_sms(order)

#         mock_initialize.assert_called_once_with("mock_username", "mock_api_key")
#         mock_send.assert_called_once_with(
#             f"Thank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: KES {order.total_cost}.",
#             ["+254712345678"]
#         )

#     @patch("app.orders.tasks.smtplib.SMTP_SSL")
#     def test_send_order_confirmation_email(self, mock_smtp):
#         # Test case where phone number is not available
#         buyer = Buyer(phone_number=None, email="buyer@example.com")
#         order = Order(order_no="12345", total_cost=1000, buyer=buyer)

#         send_order_confirmation_sms(order)

#         mock_server = mock_smtp.return_value.__enter__.return_value
#         mock_server.login.assert_called_once_with(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
#         mock_server.sendmail.assert_called_once_with(
#             settings.DEFAULT_FROM_EMAIL,
#             "buyer@example.com",
#             f"Subject: Order Confirmation\n\nThank you for shopping with us! Your order tracking no. is {order.order_no}. Total Amount: KES {order.total_cost}."
#         )
#         mock_server.quit.assert_called_once()

#     @patch("app.orders.tasks.smtplib.SMTP_SSL")
#     def test_send_order_confirmation_email_failure(self, mock_smtp):
#         # Test case where sending email fails
#         buyer = Buyer(phone_number=None, email="buyer@example.com")
#         order = Order(order_no="12345", total_cost=1000, buyer=buyer)

#         mock_server = mock_smtp.return_value.__enter__.return_value
#         mock_server.sendmail.side_effect = smtplib.SMTPException("Failed to send email")

#         with self.assertLogs("app.orders.tasks", level="ERROR") as cm:
#             send_order_confirmation_sms(order)
#             self.assertTrue(any("Failed to send order confirmation email: Failed to send email" in message for message in cm.output))

#         mock_server.login.assert_called_once_with(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
#         mock_server.quit.assert_called_once()
