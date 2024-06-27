from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.inventory.models import Category, Product

User = get_user_model()


class ProductCategoryViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            phone_number="+254799757242",
            name="john",
            password="adminpassword",
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_list_product_categories(self):
        # Create some sample categories
        Category.objects.create(name="Category 1")
        Category.objects.create(name="Category 2")

        url = reverse("products:categories-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Add more assertions as needed

    def test_create_product_category(self):
        url = reverse("products:categories-list")
        data = {"name": "New Category"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        # Add more assertions as needed

    # Add more test cases for other actions (update, delete) as needed


class ProductWriteViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a superuser for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            phone_number="+254799757242",
            name="john doe",
            password="adminpassword",
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_products(self):
        # Create some sample products
        Product.objects.create(
            name="Product 1", description="Description 1", price=10.99
        )
        Product.objects.create(
            name="Product 2", description="Description 2", price=19.99
        )

        url = reverse("products:admin-products-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
