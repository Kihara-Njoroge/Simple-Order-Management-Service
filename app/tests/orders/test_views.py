from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import OrderFactory, ProductFactory, UserFactory


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory(buyer=self.user)
        self.url = "/api/v1/orders/"

    def test_create_order(self):
        self.product = ProductFactory()

        order_items_data = [
            {
                "product": self.product.id,
                "quantity": 1,
            },
        ]

        data = {
            "buyer": self.user.id,
            "status": "COMPLETED",
            "order_items": order_items_data,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_checkout_order(self):
        self.client.force_authenticate(user=self.user)
        self.order.status = "PENDING"
        self.order.save()
        response = self.client.post(
            f"{self.url}{self.order.id}/checkout/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Order Completed successfully. You will receive a confirmation message shortly.",
        )

        self.order.status = "COMPLETED"
        self.order.save()
        response = self.client.post(
            f"{self.url}{self.order.id}/checkout/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "This order has already been completed."
        )
