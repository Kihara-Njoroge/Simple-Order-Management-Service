from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"categories", views.ProductCategoryViewSet, basename="categories")
router.register(
    r"customer-products", views.ProductReadViewSet, basename="customer-products"
)
router.register(r"admin-products", views.ProductWriteViewSet, basename="admin-products")

urlpatterns = [path("", include(router.urls))]

app_name = "products"
