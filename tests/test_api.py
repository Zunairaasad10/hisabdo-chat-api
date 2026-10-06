from fastapi.testclient import TestClient
from app.main import app, llm

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_503_without_api_key(monkeypatch):
    monkeypatch.setattr(llm, "client", None)
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test-1", "message": "What is profit?"},
    )
    assert response.status_code == 503
    assert "GROQ_API_KEY" in response.json()["detail"]
