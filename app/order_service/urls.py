from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import DefaultRouter

from .views import SpectacularRapiDocView

router = DefaultRouter()

base_urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path("docs/", SpectacularRapiDocView.as_view(), name="api-docs"),
            ]
        ),
    ),
]

urlpatterns = base_urlpatterns + router.urls
