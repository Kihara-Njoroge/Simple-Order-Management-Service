from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory

from app.orders.models import OrderItem


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


class OrderItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory(buyer=self.user)
        self.product = ProductFactory()
        self.order_item = OrderItemFactory(order=self.order, product=self.product)
        self.url = f"/api/v1/orders/{self.order.id}/order-items/"
        self.client.force_authenticate(user=self.user)

    def test_retrieve_order_items(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_order_item(self):
        url = f"{self.url}{self.order_item.id}/"
        data = {"product": self.product.id, "quantity": 1}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 1)

    def test_delete_order_item(self):
        url = f"{self.url}{self.order_item.id}/"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())
