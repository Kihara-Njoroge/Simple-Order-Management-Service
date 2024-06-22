from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import DefaultRouter

from .views import oauth_receiver_view, rapidoc_view

router = DefaultRouter()

base_urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path("docs/", rapidoc_view, name="api-docs"),
                path(
                    "docs/oauth-receiver.html",
                    oauth_receiver_view,
                    name="oauth-receiver",
                ),
                re_path(r"^docs/.*$", rapidoc_view, name="api-docs-catchall"),
                path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
                path("", include("app.users.urls")),
            ]
        ),
    ),
]

urlpatterns = base_urlpatterns + router.urls
