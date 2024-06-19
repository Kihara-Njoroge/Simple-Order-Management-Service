import pytest


@pytest.fixture(scope="session")
def dummy_test():
    print("Running Health Check...")
    assert True
