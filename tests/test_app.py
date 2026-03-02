from fastapi.testclient import TestClient
from src.app import app, activities
import pytest
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the activities dict before each test for isolation
    original = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Recreational and competitive soccer",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater production and dramatic performance",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["benjamin@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Advanced mathematics competition and problem solving",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    }
    activities.clear()
    activities.update(copy.deepcopy(original))

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12

def test_signup_success():
    resp = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert resp.status_code == 200
    assert "Signed up test@mergington.edu for Chess Club" in resp.json()["message"]
    # Check participant added
    resp2 = client.get("/activities")
    assert "test@mergington.edu" in resp2.json()["Chess Club"]["participants"]

def test_signup_duplicate():
    resp = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"

def test_signup_activity_not_found():
    resp = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"

def test_unregister_success():
    resp = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
    assert resp.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" in resp.json()["message"]
    # Check participant removed
    resp2 = client.get("/activities")
    assert "michael@mergington.edu" not in resp2.json()["Chess Club"]["participants"]

def test_unregister_not_found():
    resp = client.delete("/activities/Chess%20Club/unregister?email=notfound@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found"

def test_unregister_activity_not_found():
    resp = client.delete("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
