from fastapi.testclient import TestClient
from app.back.main import app  # <– changement important

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
