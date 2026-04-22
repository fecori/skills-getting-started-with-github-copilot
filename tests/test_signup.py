"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_for_activity_success(client):
    """Test successfully signing up for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up alice@mergington.edu for Basketball Team"
    }
    
    # Verify the student was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "alice@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup fails when activity doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(client):
    """Test signup fails when student is already registered"""
    # First signup
    client.post(
        "/activities/Swimming Club/signup",
        params={"email": "bob@mergington.edu"}
    )
    
    # Try to signup again
    response = client.post(
        "/activities/Swimming Club/signup",
        params={"email": "bob@mergington.edu"}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full(client):
    """Test signup fails when activity is at max capacity"""
    # Art Studio has max 15 participants, start with 0
    # Sign up 15 students
    for i in range(15):
        client.post(
            "/activities/Art Studio/signup",
            params={"email": f"student{i}@mergington.edu"}
        )
    
    # Try to sign up one more
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": "extra@mergington.edu"}
    )
    assert response.status_code == 400
    assert "is full" in response.json()["detail"]


def test_signup_multiple_activities_same_email(client):
    """Test that a student can sign up for multiple activities"""
    email = "multi@mergington.edu"
    
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Drama Club"]["participants"]
