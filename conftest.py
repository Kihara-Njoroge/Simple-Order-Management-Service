import pytest


@pytest.fixture(scope="session")
def dummy_test():
    print("Running dummy test...")
    # Perform dummy test actions here, such as asserting trivial conditions
    assert True
