from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.json().get('message') == "Mini Project By MPP"