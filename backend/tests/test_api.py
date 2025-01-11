import pytest
import os
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.invoice_parser import InvoiceParser
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture
def client():
    # Mock environment variables for testing
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test_credentials.json"
    os.environ["DEBUG"] = "True"
    os.environ["ALLOWED_EXTENSIONS"] = ".jpg,.jpeg,.png,.pdf"
    os.environ["MAX_FILE_SIZE"] = "10485760"  # 10MB
    
    # Mock Google Cloud Vision client
    with patch('google.cloud.vision.ImageAnnotatorClient') as mock_client:
        mock_client.return_value = MagicMock()
        yield TestClient(app)

@pytest.mark.asyncio
async def test_upload_invoice_image(client):
    # Create temporary file
    with open("temp.jpg", "wb") as f:
        f.write(b"dummy image data")
    
    try:
        with open("temp.jpg", "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("temp.jpg", f, "image/jpeg")}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "invoice_number" in data
            assert "date" in data
            assert "total_amount" in data
    finally:
        # Clean up temporary file
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")

@pytest.mark.asyncio
async def test_upload_invoice_pdf(client):
    # Create temporary file
    with open("temp.pdf", "wb") as f:
        f.write(b"dummy pdf data")
    
    try:
        with open("temp.pdf", "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("temp.pdf", f, "application/pdf")}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "invoice_number" in data
            assert "date" in data
            assert "total_amount" in data
    finally:
        # Clean up temporary file
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")

@pytest.mark.asyncio
async def test_upload_invalid_file_type(client):
    # Create temporary file
    with open("temp.txt", "w") as f:
        f.write("invalid file content")
    
    try:
        with open("temp.txt", "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("temp.txt", f, "text/plain")}
            )
            
            assert response.status_code == 400
            assert "detail" in response.json()
    finally:
        # Clean up temporary file
        if os.path.exists("temp.txt"):
            os.remove("temp.txt")

@pytest.mark.asyncio
async def test_upload_large_file(client):
    # Create large temporary file
    large_data = b"a" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    with open("large_temp.pdf", "wb") as f:
        f.write(large_data)
    
    try:
        with open("large_temp.pdf", "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("large_temp.pdf", f, "application/pdf")}
            )
            
            assert response.status_code == 413
            assert "detail" in response.json()
    finally:
        # Clean up temporary file
        if os.path.exists("large_temp.pdf"):
            os.remove("large_temp.pdf")

@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
