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


@pytest.mark.django_db
def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"


@pytest.mark.django_db
def test_user_short_name(base_user):
    """Test that the user models get_short_name method works"""
    short_name = f"{base_user.username}"
    assert base_user.get_short_name() == short_name


@pytest.mark.django_db
def test_base_user_email_is_normalized(base_user):
    """Test that a new user's email is normalized"""
    email = base_user.email
    assert base_user.email == email.lower()


@pytest.mark.django_db
def test_super_user_email_is_normalized(super_user):
    """Test that an admin user's email is normalized"""
    email = super_user.email
    assert super_user.email == email.lower()


@pytest.mark.django_db
def test_create_user_with_no_email():
    """Test that creating a new user with no email address raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_user(
            username="test",
            email="",
            name="John",
            password="password",
        )
    assert str(err.value) == "Email is required!"


@pytest.mark.django_db
def test_create_user_with_no_username():
    """Test that creating a new user with no username raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_user(
            username="",
            email="test@example.com",
            name="John",
            password="password",
        )
    assert str(err.value) == "users must provide a username"


@pytest.mark.django_db
def test_create_user_with_no_name():
    """Test that creating a new user with no name raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_user(
            username="test",
            email="test@example.com",
            name="",
            password="password",
        )
    assert str(err.value) == "users must provide a name"


@pytest.mark.django_db
def test_create_superuser_with_no_email():
    """Test creating a superuser without an email address raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_superuser(
            username="admin",
            name="Admin",
            password="password",
            email=None,
        )
    assert str(err.value) == "Email is required for admin account!"


@pytest.mark.django_db
def test_create_superuser_with_no_password():
    """Test creating a superuser without a password raises an error"""
    with pytest.raises(ValueError) as err:
        User.objects.create_superuser(
            username="admin",
            name="Admin",
            password=None,
            email="admin@example.com",
        )
    assert str(err.value) == "Superuser must have a password."
