from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]

    try:
        activity["participants"] = ["student@example.com"]

        response = client.post(f"/activities/{activity_name}/signup?email=student@example.com")

        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"
    finally:
        activity["participants"] = original_participants


def test_delete_signup_removes_participant():
    activity_name = "Programming Class"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]

    try:
        activity["participants"] = ["first@example.com", "second@example.com"]

        response = client.delete(f"/activities/{activity_name}/signup?email=first@example.com")

        assert response.status_code == 200
        assert response.json()["message"] == "Removed first@example.com from Programming Class"
        assert activity["participants"] == ["second@example.com"]
    finally:
        activity["participants"] = original_participants
