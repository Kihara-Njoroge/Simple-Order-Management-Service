from datetime import datetime, timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# custom user manager
class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    # user
    def create_user(
        self, username, name, email, password, phone_number=None, **extra_fields
    ):
        if not username:
            raise ValueError(_("users must provide a username"))
        if not name:
            raise ValueError(_("users must provide a name"))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("an email address is required"))

        user = self.model(
            username=username,
            name=name,
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        extra_fields.setdefault("if_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, name, phone_number, email, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        if not password:
            raise ValueError(_("Superuser must have a password"))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("an email address is required for admin account"))

        user = self.create_user(
            username, name, phone_number, email, password, **extra_fields
        )
        user.save(using=self._db)
        return user
