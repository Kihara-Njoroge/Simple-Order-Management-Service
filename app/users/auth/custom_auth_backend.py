import logging
import smtplib

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from django.utils import timezone
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.utils import absolutify
from rest_framework.authtoken.models import Token

LOGGER = logging.getLogger(__name__)


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """Custom OIDC authentication backend."""

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""

        self.request = request
        if not self.request:
            return None

        state = self.request.GET.get("state")
        code = self.request.GET.get("code")
        nonce = kwargs.pop("nonce", None)

        if not code or not state:
            return None

        reverse_url = self.get_settings(
            "OIDC_AUTHENTICATION_CALLBACK_URL", "oidc_authentication_callback"
        )

        token_payload = {
            "client_id": self.OIDC_RP_CLIENT_ID,
            "client_secret": self.OIDC_RP_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": absolutify(self.request, reverse(reverse_url)),
        }

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get("id_token")
        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")

        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            try:
                return self.get_or_create_user(access_token, id_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.warning("failed to get or create user: %s", exc)
                return None

        return None

    def get_or_create_user(self, access_token, id_token, payload):
        """Get or create a user."""
        try:
            user = self.UserModel.objects.get(email=payload["email"])
        except self.UserModel.DoesNotExist:
            user_info = {
                "username": payload.get("preferred_username", payload.get("sub")),
                "name": payload.get("name", ""),
                "email": payload.get("email"),
                "password": "123456",
            }
            user = self.UserModel.objects.create_user(**user_info)
            self.send_welcome_email(user)
        self.store_tokens(user, access_token)

        return user

    def send_welcome_email(self, user):
        subject = "Account setup completion"
        message = f"Hi {user.name},\n\nThank you for signing in. We are glad to have you with us. Please login to update your phone number for a better experience. Your temporary password is 123456."
        from_email = settings.DEFAULT_FROM_EMAIL
        body = f"Subject: {subject}\n\n{message}"
        recipient_list = [user.email]

        try:
            # For SSL connection (port 465)
            server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
            server.login(from_email, settings.EMAIL_HOST_PASSWORD)

            # Or, for TLS connection (port 587)
            # server = smtplib.SMTP("smtp.zoho.com", 587)
            # server.starttls()
            # server.login(from_email, settings.EMAIL_HOST_PASSWORD)

            for email in recipient_list:
                server.sendmail(settings.DEFAULT_FROM_EMAIL, email, body)

            server.quit()
        except Exception as e:
            LOGGER.error(f"Failed to send welcome email to {user.email}: {e}")

    def store_tokens(self, user, access_token):
        """
        Stores the tokens in the database.

        """
        # Delete any existing tokens for the user
        Token.objects.filter(user=user).delete()

        # Create new token
        token = Token.objects.create(
            user=user, key=access_token, created=timezone.now()
        )
        token.save()
