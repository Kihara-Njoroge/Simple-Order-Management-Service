import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"), max_length=30, null=True, blank=True
    )

    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # declare username field and required fields
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    objects = CustomUserManager()

    # define meta class
    class Meta:
        app_label = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # define string representation of the model
    def __str__(self):
        return self.username

    # define properties
    @property
    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username
