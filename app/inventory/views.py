from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product
from .serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for product categories.
    """

    queryset = Category.objects.all()
    serializer_class = ProductCategoryReadSerializer
    # permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        category_name = request.data.get("name")
        if Category.objects.filter(name=category_name).exists():
            return Response(
                {"detail": "Category already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        category.delete()
        return Response(
            {"message": "Category deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProductReadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Products reading viewset (customers).
    """

    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductWriteViewSet(viewsets.ModelViewSet):
    """
    Products CRUD operations. (Admin)
    """

    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    ##permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        product_name = request.data.get("name")
        print(product_name)
        if Product.objects.filter(name=product_name).exists():
            return Response(
                {"detail": "Product already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if not request.user.is_staff:
        #     return Response(
        #         {"detail": "You do not have permission to create products."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to update products."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete products."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
