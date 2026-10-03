from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "LegalEase"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_demo_or_configured():
    payload = {
        "document_type": "NDA",
        "parties": "Alice (Disclosing Party), Acme Ltd (Receiving Party)",
        "terms": "Confidentiality; Return information upon termination",
        "dates": "October 1, 2026",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["document"].strip()
    assert "NDA" in data["document"]
