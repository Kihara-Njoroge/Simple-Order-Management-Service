from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from app.users.models import (  # Update this import to match your user model location
    User,
)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?response_type=code"
            f"&client_id={settings.OIDC_RP_CLIENT_ID}"
            f"&redirect_uri={request.build_absolute_uri(settings.LOGIN_REDIRECT_URL)}"
            f"&scope=openid%20email%20profile"
        )
        return redirect(google_auth_url)


class OAuth2CallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response(
                {"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Exchange the authorization code for an access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.OIDC_RP_CLIENT_ID,
            "client_secret": settings.OIDC_RP_CLIENT_SECRET,
            "redirect_uri": request.build_absolute_uri(settings.LOGIN_REDIRECT_URL),
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_url, data=token_data)
        token_response_data = token_response.json()

        if "error" in token_response_data:
            return Response(token_response_data, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response_data["access_token"]

        # Get user info from Google
        userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
        userinfo_response = requests.get(
            userinfo_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo = userinfo_response.json()

        if "error" in userinfo:
            return Response(userinfo, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate or create the user
        email = userinfo.get("email")
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = email
            user.first_name = userinfo.get("given_name", "")
            user.last_name = userinfo.get("family_name", "")
            user.set_unusable_password()
            user.save()

        if user is not None and user.is_active:
            Token.objects.filter(user=user).delete()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            token.expires = timezone.now() + timedelta(hours=24)
            token.save()

            response = Response({"token": token.key}, status=status.HTTP_200_OK)
            response.set_cookie(key="token", value=token.key, httponly=True)

            return response
        elif user is not None:
            return Response(
                {"error": "User is not active"}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
