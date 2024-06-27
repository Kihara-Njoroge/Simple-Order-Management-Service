from decimal import Decimal

from django.test import TestCase

from app.inventory.models import Product
from app.orders.models import Order, OrderItem
from app.orders.serializers import OrderItemSerializer
from app.users.models import User


class OrderItemSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.product = Product.objects.create(name="Test Product", stock=10, price=20)
        self.order = Order.objects.create(buyer=self.user, status=Order.PENDING)

    def test_order_item_serialization(self):
        order_item = OrderItem.objects.create(
            product=self.product, quantity=3, order=self.order
        )
        serializer = OrderItemSerializer(order_item)
        expected_data = {
            "id": order_item.id,
            "order": self.order.id,
            "product": self.product.id,
            "product_name": self.product.name,
            "quantity": 3,
            "price": Decimal("20.00"),
            "cost": Decimal("60.00"),
            "created_at": order_item.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": order_item.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        self.assertEqual(serializer.data, expected_data)
