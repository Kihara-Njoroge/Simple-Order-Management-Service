from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from django.views.decorators.cache import never_cache

from users.auth.oidc_logout import oidc_logout


User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    @extend_schema(description="Add a user")
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully.", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description="Fetch all users")
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(description="Get a user by id")
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)

    @extend_schema(description="Update a user")
    def update(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully.", "user": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description="Update a user")
    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully.", "user": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description="Delete a user")
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class CustomLogoutAPIView(APIView):
    """
    API endpoint that handles user logout

    """

    permission_classes = [IsAuthenticated]

    @never_cache
    def post(self, request, *args, **kwargs):
        oidc_logout(request)
        logout(request)
        return Response(
            {"detail": "Logged out successfully"}, status=status.HTTP_200_OK
        )


# authenticate user
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:  # Check if the user is active
                # Delete the existing token (if any)
                Token.objects.filter(user=user).delete()

                login(request, user)

                # Create a new token with an expiration time
                token, created = Token.objects.get_or_create(user=user)
                token.expires = timezone.now() + timedelta(
                    hours=24
                )  # Set expiration time
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
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = None

#     def post(self, request):
#         # Delete the existing token and related cookies
#         user = request.user
#         Token.objects.filter(user=user).delete()

#         # Logout the user
#         logout(request)

#         response = Response(
#             {"message": "Logged out successfully"}, status=status.HTTP_200_OK
#         )

#         # Delete the token cookie
#         response.delete_cookie("token")

#         return response
