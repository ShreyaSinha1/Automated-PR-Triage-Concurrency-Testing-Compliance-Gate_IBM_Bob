from fastapi.testclient import TestClient
import pytest
import os
from app.main import app

# Inject a known test token into the environment so verify_token resolves correctly.
_TEST_TOKEN = "test_token_for_pytest"
os.environ["INTERNAL_SYSTEM_API_KEY"] = _TEST_TOKEN

client = TestClient(app)

_AUTH_HEADERS = {"Authorization": f"Bearer {_TEST_TOKEN}"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_compute_metrics():
    # Authenticated request — reaches the ZeroDivisionError path and expects structured 500.
    response = client.get("/api/v1/compute?factor=0", headers=_AUTH_HEADERS)
    assert response.status_code == 500  # Expecting proper structured failure handling
    assert response.json()["detail"] is not None
