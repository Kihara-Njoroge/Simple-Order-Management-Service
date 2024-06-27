from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from app.users.auth.custom_auth_backend import CustomOIDCAuthenticationBackend
from app.users.auth.oidc_logout import oidc_logout

User = get_user_model()


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="dummy",
            email="dummy@gmail.com",
            phone_number="+254799757242",
            name="dummy",
            password="Passw0rd@1",
        )
        self.user_url = f"/api/v1/users/{self.user.id}/"

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@gmail.com",
            "phone_number": "+254799757243",
            "name": "new",
            "password": "Passw0rd@1",
        }
        response = self.client.post("/api/v1/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        user = User.objects.get(email=data["email"])
        self.assertEqual(user.username, data["username"])

    def test_partial_update_user(self):
        data = {"name": "Partial"}
        response = self.client.patch(self.user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["name"], "Partial")

    def test_update_user(self):
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "phone_number": "+254712345679",
            "name": "Updated",
        }
        response = self.client.put(self.user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["name"], "Updated")
        self.assertEqual(response.data["user"]["phone_number"], "+254712345679")

    def test_list_users(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_user(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.user.id))

    def test_retrieve_nonexistent_user(self):
        non_existent_url = "/api/v1/users/8c8ff04a-b949-4415-8d1d-f24f348a16c9/"
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_user(self):
        login_data = {
            "email": self.user.email,
            "password": "Passw0rd@1",
        }
        response = self.client.post("/api/v1/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        login_data = {
            "email": self.user.email,
            "password": "InvalidPassword",
        }
        response = self.client.post("/api/v1/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)


class OIDCLogoutTestCase(TestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(
            username="dummy",
            email="dummy@gmail.com",
            phone_number="+254799757242",
            name="dummy",
            password="Passw0rd@1",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_oidc_logout(self):
        request = HttpRequest()
        request.user = self.user
        request.session = MagicMock()
        request.session.get.return_value = "mock_token"
        oidc_logout(request)


class CustomOIDCAuthenticationBackendTestCase(TestCase):
    def setUp(self):
        self.backend = CustomOIDCAuthenticationBackend()
        self.factory = APIRequestFactory()

    @patch.object(CustomOIDCAuthenticationBackend, "get_token")
    @patch.object(CustomOIDCAuthenticationBackend, "verify_token")
    @patch.object(CustomOIDCAuthenticationBackend, "get_or_create_user")
    def test_send_welcome_email_and_store_tokens(
        self, mock_get_or_create_user, mock_verify_token, mock_get_token
    ):
        # Mock token_info and payload for simulate authentication flow
        token_info = {
            "id_token": "mock_id_token",
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
        }
        payload = {
            "email": "testuser@example.com",
            "preferred_username": "testuser",
            "name": "Test User",
            "password": "123456",
        }

        # Set the return values of the mocked methods
        mock_get_token.return_value = token_info
        mock_verify_token.return_value = payload

        # Create a mock user object to be returned by get_or_create_user
        mock_user = User.objects.create_user(
            username="testuser",
            name="Test User",
            email="testuser@example.com",
            password="password",
        )
        mock_get_or_create_user.return_value = mock_user

        # Create a mock request to trigger authentication
        request = self.factory.get(
            reverse("oidc_authentication_init"),
            data={"state": "mock_state", "code": "mock_code"},
        )
        request.session = MagicMock()
        request.session.get.return_value = "mock_nonce"
