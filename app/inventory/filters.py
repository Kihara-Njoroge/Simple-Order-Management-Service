from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    category_name = filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains",
    )
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_stock = filters.NumberFilter(field_name="stock", lookup_expr="gte")
    max_stock = filters.NumberFilter(field_name="stock", lookup_expr="lte")

    class Meta:
        model = Product
        fields = [
            "product_name",
            "category_name",
            "min_price",
            "max_price",
            "min_stock",
            "max_stock",
        ]
