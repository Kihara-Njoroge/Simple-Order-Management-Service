from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

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
        print("DAATA", data)
        response = self.client.put(self.user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["name"], "Updated")
        self.assertEqual(response.data["user"]["phone_number"], "+254712345679")

    def test_delete_user(self):
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            username="testuser",
            name="John",
            phone_number="+254799757242",
            is_active=True,
        )
        self.login_url = "/api/v1/login/"
        self.client = APIClient()

    def test_login(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.cookies["token"].value, response.data["token"])

    def test_login_inactive_user(self):
        # Deactivate the user
        self.user.is_active = False
        self.user.save()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("error" in response.data)

    def test_login_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "invalidpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("error" in response.data)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            username="testuser",
            name="John",
            phone_number="+254799757242",
            is_active=True,
        )
        self.client = APIClient()

    def test_logout_success(self):
        # Authenticate the user by creating a token
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Logout the user
        response = self.client.post("/api/v1/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")

    def test_logout_failure_unauthenticated(self):
        # Try to logout without authentication
        response = self.client.post("/api/v1/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
