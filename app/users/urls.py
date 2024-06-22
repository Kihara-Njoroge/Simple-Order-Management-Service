from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
    path("auth/callback/", views.OAuth2CallbackView.as_view(), name="oauth2_callback"),
]

app_name = "users"
