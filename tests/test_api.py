from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_generate_email():
    with patch(
        "backend.main.generate_email",
        return_value="เรื่อง: ขอเลื่อนนัดประชุม\nเรียน อาจารย์"
    ):
        response = client.post(
            "/generate-email",
            json={
                "user_prompt": "ขอเลื่อนนัดประชุม",
                "tone": "เป็นทางการ",
                "email_type": "ติดต่ออาจารย์"
            }
        )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "ขอเลื่อนนัดประชุม" in response.json()["email"]
