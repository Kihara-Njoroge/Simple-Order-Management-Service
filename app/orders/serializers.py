import uuid

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer class for serializing order items.
    """

    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "product_name",
            "quantity",
            "price",
            "cost",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("order",)

    def validate(self, data):
        """
        Validate order item data.
        """
        order_quantity = data["quantity"]
        product_quantity = data["product"].stock

        order_id = self.context["view"].kwargs.get("order_id")
        product = data["product"]
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            raise ValidationError(
                {"quantity": _("Ordered quantity is more than the stock.")}
            )

        if not self.instance and current_item.exists():
            raise ValidationError(
                {"product": _("Product already exists in your order.")}
            )

        return data

    @extend_schema_field(str)
    def get_price(self, obj):
        return obj.product.price

    @extend_schema_field(str)
    def get_cost(self, obj):
        return obj.cost

    @extend_schema_field(str)
    def get_product_name(self, obj):
        return obj.product.name


class OrderReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading orders.
    """

    buyer = serializers.CharField(source="buyer.get_full_name", read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "order_no",
            "order_items",
            "total_cost",
            "status",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(str)
    def get_total_cost(self, obj):
        return obj.total_cost


class OrderWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and updating orders.
    """

    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "status",
            "order_items",
            "created_at",
            "updated_at",
            "order_no",
        )
        read_only_fields = ("status", "order_no")

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        # Generate a unique order number
        validated_data["order_no"] = str(uuid.uuid4())
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_items", None)
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        if order_items_data:
            for item_data in order_items_data:
                order_item = OrderItem.objects.filter(
                    order=instance, product=item_data["product"]
                ).first()
                if order_item:
                    order_item.quantity = item_data.get("quantity", order_item.quantity)
                    order_item.save()
                else:
                    OrderItem.objects.create(order=instance, **item_data)

        return instance
