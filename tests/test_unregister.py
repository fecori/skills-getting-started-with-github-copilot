"""Tests for POST /activities/{activity_name}/unregister endpoint"""

import pytest


def test_unregister_success(client):
    """Test successfully unregistering from an activity"""
    email = "charlie@mergington.edu"
    
    # First sign up
    client.post(
        "/activities/Swimming Club/signup",
        params={"email": email}
    )
    
    # Then unregister
    response = client.post(
        "/activities/Swimming Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Swimming Club"
    }
    
    # Verify the student was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Swimming Club"]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister fails when activity doesn't exist"""
    response = client.post(
        "/activities/Fake Activity/unregister",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_student_not_registered(client):
    """Test unregister fails when student is not signed up"""
    response = client.post(
        "/activities/Debate Team/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_from_initial_participants(client):
    """Test unregistering a student who was an initial participant"""
    email = "michael@mergington.edu"
    
    # Verify they're initially in Chess Club
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    
    # Unregister
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify they're no longer there
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Chess Club"]["participants"]


def test_signup_after_unregister(client):
    """Test that a student can re-register after unregistering"""
    email = "rejoiner@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    
    # Unregister
    client.post(
        "/activities/Drama Club/unregister",
        params={"email": email}
    )
    
    # Sign up again
    response = client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Drama Club"]["participants"]
