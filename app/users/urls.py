from django.urls import include, path
from rest_framework.routers import DefaultRouter
from mozilla_django_oidc import views as oidc_views

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
]

app_name = "users"
