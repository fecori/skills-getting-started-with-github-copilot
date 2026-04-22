"""Tests for GET /activities endpoint"""

import pytest


def test_get_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_activities_have_correct_structure(client):
    """Test that each activity has the expected structure"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Verify types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_have_initial_participants(client):
    """Test that some activities have initial participants"""
    response = client.get("/activities")
    activities = response.json()
    
    # These should have initial participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    assert len(activities["Programming Class"]["participants"]) == 2
    assert len(activities["Gym Class"]["participants"]) == 2
    
    # These should be empty
    assert len(activities["Basketball Team"]["participants"]) == 0
    assert len(activities["Swimming Club"]["participants"]) == 0
