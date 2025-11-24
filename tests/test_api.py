from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_dict():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    test_email = "pytest.temp.user@example.com"

    # Ensure test email not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()
    participants_before = list(before[activity_name]["participants"])
    if test_email in participants_before:
        participants_before.remove(test_email)

    # Sign up the test user
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Verify participant appears
    resp2 = client.get("/activities")
    after = resp2.json()
    participants_after = after[activity_name]["participants"]
    assert test_email in participants_after

    # Now unregister
    del_resp = client.delete(f"/activities/{activity_name}/participants?email={test_email}")
    assert del_resp.status_code == 200
    assert "Unregistered" in del_resp.json().get("message", "")

    # Verify participant removed
    resp3 = client.get("/activities")
    final = resp3.json()
    participants_final = final[activity_name]["participants"]
    assert test_email not in participants_final


if __name__ == "__main__":
    pytest.main([__file__])
