import os
import sys

# Ajoute le dossier parent (app/back) au PYTHONPATH, peu importe d'où pytest est lancé
CURRENT_DIR = os.path.dirname(__file__)
BACK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACK_DIR not in sys.path:
    sys.path.append(BACK_DIR)

from fastapi.testclient import TestClient
from main import app   # <= main.py dans app/back

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
