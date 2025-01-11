import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.config import settings

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_invoice_processing_flow(client):
    # Test data
    test_file = "backend/tests/test_data/sample_invoice.jpg"
    
    # Upload file
    with open(test_file, "rb") as f:
        response = client.post(
            "/api/v1/invoices/upload",
            files={"file": ("invoice.jpg", f, "image/jpeg")}
        )
    
    assert response.status_code == 200
    response_data = response.json()
    
    # Verify response structure
    assert "invoice_id" in response_data
    assert "status" in response_data
    assert "processed_data" in response_data
    
    # Get processed invoice
    invoice_id = response_data["invoice_id"]
    response = client.get(f"/api/v1/invoices/{invoice_id}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "processed"

@pytest.mark.skipif(
    not settings.TEST_REDIS,
    reason="Requires Redis connection"
)
def test_redis_connection(client):
    response = client.get("/api/v1/redis/health")
    assert response.status_code == 200
    assert response.json() == {"redis": "connected"}
