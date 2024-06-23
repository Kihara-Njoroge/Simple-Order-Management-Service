from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"categories", views.ProductCategoryViewSet)
router.register(r"customer-products", views.ProductReadViewSet)
router.register(r"admin-products", views.ProductWriteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "products"
