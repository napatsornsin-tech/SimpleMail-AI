from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)


# 1. Home Test
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


# 2. Generate Email Test
def test_generate_email():
    with patch(
        "backend.main.generate_email",
        return_value="เรื่อง: ขอเลื่อนนัดประชุม"
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


# 3. Empty Input Test
def test_empty_input():
    with patch(
        "backend.main.generate_email",
        return_value="กรุณาระบุรายละเอียด"
    ):
        response = client.post(
            "/generate-email",
            json={
                "user_prompt": "",
                "tone": "เป็นทางการ",
                "email_type": "ทั่วไป"
            }
        )

    assert response.status_code == 200


# 4. Missing Field Test
def test_missing_field():
    response = client.post(
        "/generate-email",
        json={
            "tone": "เป็นทางการ"
        }
    )

    assert response.status_code == 422


# 5. Email Type Test
def test_email_type():
    with patch(
        "backend.main.generate_email",
        return_value="เรียน ผู้จัดการฝ่ายบุคคล"
    ) as mock_generate:

        response = client.post(
            "/generate-email",
            json={
                "user_prompt": "ต้องการสมัครงาน",
                "tone": "เป็นทางการ",
                "email_type": "สมัครงาน"
            }
        )

    assert response.status_code == 200
    assert mock_generate.call_args.kwargs["email_type"] == "สมัครงาน"

