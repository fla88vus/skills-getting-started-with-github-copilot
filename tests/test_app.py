import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data, "Activities list should not be empty."

def test_signup_and_unregister():
    # Get an activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities))
    test_email = "pytest@example.com"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup.status_code == 200
    assert "message" in signup.json()

    # Unregister
    unregister = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister.status_code == 200
    assert "message" in unregister.json()

    # Unregister again (should fail)
    unregister2 = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister2.status_code == 400
    assert "detail" in unregister2.json()
