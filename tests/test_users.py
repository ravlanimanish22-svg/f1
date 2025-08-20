from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users_list():
    # Register and login as admin
    client.post(
        "/v1/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass",
            "role": "admin",
            "is_admin": True
        }
    )

    response = client.post(
        "/v1/auth/token",
        data={"username": "admin", "password": "adminpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Call users endpoint with auth
    response = client.get("/v1/admin/users", headers=headers)
    assert response.status_code == 200
