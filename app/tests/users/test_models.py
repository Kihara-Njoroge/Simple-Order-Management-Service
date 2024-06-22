import pytest
from pytest_factoryboy import register
from tests.factories import UserFactory

from app.users.models import User

register(UserFactory)


@pytest.fixture
def base_user(db, user_factory):
    return user_factory.create()


@pytest.fixture
def super_user(db, user_factory):
    return user_factory.create(is_staff=True, is_superuser=True)


def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"


def test_user_short_name(base_user):
    """Test that the user models get_short_name method works"""
    short_name = f"{base_user.username}"
    assert base_user.get_short_name() == short_name


def test_base_user_email_is_normalized(base_user):
    """Test that a new user's email is normalized"""
    email = base_user.email
    assert base_user.email == email.lower()


def test_super_user_email_is_normalized(super_user):
    """Test that an admin user's email is normalized"""
    email = super_user.email
    assert super_user.email == email.lower()


def test_create_user_with_no_email():
    """Test that creating a new user with no email address raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_user(
            username="test",
            email="",
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            password="password",
        )
    assert str(err.value) == "Email is required."


def test_create_use_with_no_username():
    """Test that creating a new user with no username raises an error"""
    with pytest.raises(TypeError) as err:
        User.objects.create_user(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            password="password",
        )
    assert (
        str(err.value)
        == "CustomUserManager.create_user() missing 1 required positional argument: 'username'"
    )


def test_create_use_with_no_phone_number():
    """Test that creating a new user with no phone number raises an error"""
    with pytest.raises(TypeError) as err:
        User.objects.create_user(
            username="test",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="password",
        )
    assert (
        str(err.value)
        == "CustomUserManager.create_user() missing 1 required positional argument: 'phone_number'"
    )


def test_create_user_with_no_firstname():
    """Test creating a new user without a first name raises an error"""
    with pytest.raises(TypeError) as err:
        User.objects.create_user(
            username="test",
            email="test@example.com",
            last_name="Doe",
            phone_number="1234567890",
            password="password",
        )
    assert (
        str(err.value)
        == "CustomUserManager.create_user() missing 1 required positional argument: 'first_name'"
    )


def test_create_user_with_no_lastname():
    """Test creating a new user without a last name raises an error"""
    with pytest.raises(TypeError) as err:
        User.objects.create_user(
            username="test",
            email="test@example.com",
            first_name="John",
            phone_number="1234567890",
            password="password",
        )
    assert (
        str(err.value)
        == "CustomUserManager.create_user() missing 1 required positional argument: 'last_name'"
    )


def test_create_superuser_with_no_email():
    """Test creating a superuser without an email address raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_superuser(
            username="admin",
            first_name="Admin",
            last_name="User",
            phone_number="1234567890",
            password="password",
            email=None,
        )
    assert str(err.value) == "Email is required for admin account."


def test_create_superuser_with_no_password():
    """Test creating a superuser without a password raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_superuser(
            username="admin",
            first_name="Admin",
            last_name="User",
            phone_number="1234567890",
            password=None,
            email="admin@example.com",
        )
    assert str(err.value) == "Superuser must have a password"
