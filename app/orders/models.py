from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from app.inventory.models import Product

User = get_user_model()


class Order(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (COMPLETED, _("Completed")),
    )
    buyer = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING)
    order_no = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    # def __str__(self):
    #     return f"Order {self.order_no} by {self.buyer.get_full_name()}"

    @property
    def total_cost(self):
        """
        Total cost of all the items in an order.
        """
        return round(sum(item.cost for item in self.order_items.all()), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_orders", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("order", "product")

    # def __str__(self):
    #     return f"{self.quantity} of {self.product.name} for {self.order.buyer.get_full_name()}"

    @property
    def cost(self):
        """
        Total cost of the ordered item.
        """
        return round(self.quantity * self.product.price, 2)

    def save(self, *args, **kwargs):
        """
        Override save method to update product stock.
        """
        if self.pk:
            original = OrderItem.objects.get(pk=self.pk)
            original.product.stock += original.quantity  # Revert stock
            original.product.save()

        self.product.stock -= self.quantity  # Deduct stock
        if self.product.stock < 0:
            raise ValueError(_("Not enough stock for the product."))

        self.product.save()
        super().save(*args, **kwargs)
