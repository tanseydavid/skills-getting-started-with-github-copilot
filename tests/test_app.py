from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data) >= expected_activity_names
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Basketball Club"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]
    email = "newstudent@mergington.edu"

    try:
        activity["participants"] = []

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert activity["participants"] == [email]
    finally:
        activity["participants"] = original_participants


def test_signup_rejects_duplicate_registration():
    # Arrange
    activity_name = "Chess Club"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]
    email = "student@example.com"

    try:
        activity["participants"] = [email]

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"
    finally:
        activity["participants"] = original_participants


def test_signup_rejects_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email=student@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_signup_removes_participant():
    # Arrange
    activity_name = "Programming Class"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]
    email = "first@example.com"

    try:
        activity["participants"] = [email, "second@example.com"]

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
        assert activity["participants"] == ["second@example.com"]
    finally:
        activity["participants"] = original_participants


def test_delete_signup_rejects_student_not_signed_up():
    # Arrange
    activity_name = "Programming Class"
    activity = app_module.activities[activity_name]
    original_participants = activity["participants"][:]
    email = "not-signed-up@example.com"

    try:
        activity["participants"] = ["existing@example.com"]

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
    finally:
        activity["participants"] = original_participants
