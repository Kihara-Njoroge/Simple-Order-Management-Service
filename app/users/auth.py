from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .models import User


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        print(claims)
        user = User.objects.create(
            username=claims.get("email", ""),
            first_name=claims.get("given_name", ""),
            last_name=claims.get("family_name", ""),
            email=claims.get("email", ""),
            phone_number="+254798556767",
        )
        user.set_unusable_password()
        user.save()
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        # Again, handle phone number as needed
        user.save()
        return user
