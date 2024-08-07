import pytest
from django.db.utils import IntegrityError
from tests.factories import CategoryFactory, ProductFactory

from app.inventory.models import Category, Product, get_default_category


@pytest.mark.django_db
def test_category_creation():
    category = CategoryFactory()
    assert Category.objects.count() == 2
    assert str(category) == category.name


@pytest.mark.django_db
def test_category_slug():
    category = CategoryFactory(name="Test Category")
    assert category.slug == "test-category"


@pytest.mark.django_db
def test_category_unique_slug():
    CategoryFactory(name="Test Category 1")
    CategoryFactory(name="Test Category 2")
    category = CategoryFactory(name="Test Category 3")
    assert category.slug == "test-category-3"


@pytest.mark.django_db
def test_product_creation():
    product = ProductFactory()
    assert Product.objects.count() == 1
    assert str(product) == product.name


@pytest.mark.django_db
def test_product_slug():
    product = ProductFactory(name="Test Product")
    assert product.slug == "test-product"


@pytest.mark.django_db
def test_product_unique_slug():
    ProductFactory(name="Test Product 1")
    ProductFactory(name="Test Product 2")
    product = ProductFactory(name="Test Product 3")
    assert product.slug == "test-product-3"


@pytest.mark.django_db
def test_product_category_relation():
    category = CategoryFactory()
    product = ProductFactory(category=category)
    assert product.category == category


@pytest.mark.django_db
def test_category_name_uniqueness():
    CategoryFactory(name="Test Category")

    # Attempt to create another category with the same name
    with pytest.raises(IntegrityError):
        CategoryFactory(
            name="Test Category"
        )  # Duplicate name should raise IntegrityError


@pytest.mark.django_db
def test_product_str_representation():
    product = ProductFactory(name="Test Product")
    assert str(product) == "Test Product"


@pytest.mark.django_db
def test_default_category():
    # Get the default category using the get_default_category function
    default_category = get_default_category()

    # Check if the default category is "Others"
    assert default_category.name == "Others"
