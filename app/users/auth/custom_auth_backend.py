import logging

from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.utils import absolutify

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
            print(payload)
            self.store_tokens(access_token, id_token, refresh_token)
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
                "password": self.UserModel.objects.make_random_password(),
            }
            user = self.UserModel.objects.create_user(**user_info)
        return user

    def store_tokens(self, access_token, id_token, refresh_token):
        """Store OIDC tokens."""
        session = self.request.session

        if self.get_settings("OIDC_STORE_ACCESS_TOKEN", True):
            session["oidc_access_token"] = access_token

        if self.get_settings("OIDC_STORE_ID_TOKEN", False):
            session["oidc_id_token"] = id_token

        if self.get_settings("OIDC_STORE_REFRESH_TOKEN", True):
            session["oidc_refresh_token"] = refresh_token
