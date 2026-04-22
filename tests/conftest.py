"""Pytest configuration and fixtures for FastAPI tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, reset_activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset activities to initial state before each test"""
    reset_activities()
    yield
    # Teardown (if needed in future)
    reset_activities()
