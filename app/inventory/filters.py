from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",  # Case-insensitive partial match
    )
    category_name = filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains",  # Case-insensitive partial match
    )
    min_price = filters.NumberFilter(
        field_name="price", lookup_expr="gte"  # Greater than or equal to
    )
    max_price = filters.NumberFilter(
        field_name="price", lookup_expr="lte"  # Less than or equal to
    )
    min_stock = filters.NumberFilter(
        field_name="stock", lookup_expr="gte"  # Greater than or equal to
    )
    max_stock = filters.NumberFilter(
        field_name="stock", lookup_expr="lte"  # Less than or equal to
    )

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
