from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import DefaultRouter
from mozilla_django_oidc import views as oidc_views
from .views import SpectacularRapiDocView
from django.views.generic.base import TemplateView
from users.views import CustomLogoutAPIView, LogoutView, home


router = DefaultRouter()

base_urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                path("accounts/", include("django.contrib.auth.urls")),
                path("", include("users.urls")),
                path("", include("inventory.urls")),
                path("orders/", include("orders.urls")),
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path("docs/", SpectacularRapiDocView.as_view(), name="api-docs"),
                path(
                    "login/",
                    TemplateView.as_view(template_name="templates/login.html"),
                    name="login",
                ),
                path("home/", home, name="index"),
                path(
                    "authorization-code/authenticate/",
                    oidc_views.OIDCAuthenticationRequestView.as_view(),
                    name="oidc_authentication_init",
                ),
                path(
                    "authorization-code/callback/",
                    oidc_views.OIDCAuthenticationCallbackView.as_view(),
                    name="oidc_authentication_callback",
                ),
                path("logout/", LogoutView.as_view(), name="oidc_logout"),
            ]
        ),
    ),
]

urlpatterns = base_urlpatterns + router.urls
