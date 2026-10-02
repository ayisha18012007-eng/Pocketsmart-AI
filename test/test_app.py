from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "PocketSmart AI" in response.text


def test_login_page():

    response = client.get("/login")

    assert response.status_code == 200

    assert "Login" in response.text


def test_unauthorized_home_generation():

    response = client.post(
        "/generate-home",
        json={
            "room_type": "Bedroom",
            "room_size": "10 x 12 ft",
            "budget": 50000,
            "style": "Modern",
            "colors": "White",
            "requirements": ""
        }
    )

    assert response.status_code == 401