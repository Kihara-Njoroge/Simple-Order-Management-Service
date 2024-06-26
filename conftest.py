# fixtures
import pytest
from pytest_factoryboy import register

from app.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user
