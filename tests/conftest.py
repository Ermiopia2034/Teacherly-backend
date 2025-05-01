import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    """
    Test client fixture for FastAPI app.
    """
    with TestClient(app) as test_client:
        yield test_client
