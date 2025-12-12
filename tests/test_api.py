from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import os

print(f"Testing with DB: {settings.USE_JSON_DB}")

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_chat_no_knowledge():
    response = client.post("/api/chat", json={"query": "Hello"})
    assert response.status_code == 200
    data = response.json()
    # Expect low confidence or default message
    assert "answer" in data
    
def test_admin_login():
    response = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_crud_faq():
    # Login
    login_res = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    response = client.post("/api/faqs", json={"question": "What is AI?", "answer": "Artificial Intelligence."}, headers=headers)
    assert response.status_code == 200
    faq_id = response.json()["id"]

    # Read
    response = client.get("/api/faqs")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Chat
    chat_res = client.post("/api/chat", json={"query": "What is AI?"})
    assert chat_res.status_code == 200
    assert "Artificial Intelligence" in chat_res.json()["answer"]

    # Delete
    del_res = client.delete(f"/api/faqs/{faq_id}", headers=headers)
    assert del_res.status_code == 200
