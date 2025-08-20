from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_and_login():
    # Register user
    response = client.post(
        "/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
    )
    assert response.status_code in [200, 400]  # may fail if already exists

    # Login
    response = client.post(
        "/v1/auth/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    token = data["access_token"]

    # Current user
    response = client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
