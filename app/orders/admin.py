from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "status",
        "order_no",
        "created_at",
        "updated_at",
        "total_cost",
    )
    list_filter = ("status", "buyer")
    search_fields = (
        "order_no",
        "buyer__username",
        "buyer__name",
    )
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
