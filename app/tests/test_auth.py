import pytest
from fastapi import status
from app.database.models import User
from app.security.hashing import verify_password

# Test successful user signup and token response
def test_signup_success(client):
    response = client.post(
        "/auth/signup",
        json={"username": "newuser", "password": "newpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["username"] == "newuser"

# Test signup with a duplicate username returns error
def test_signup_duplicate_username(client, test_user):
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "password": "newpass"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Test successful login returns access token
def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

# Test login with wrong password returns unauthorized
def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Test login with nonexistent user returns unauthorized
def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "pass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Test getting current user info with valid token
def test_get_current_user(client, test_user):
    # First login to get token
    login_response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    
    # Test protected endpoint
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testuser"

# Test getting current user info with invalid token returns unauthorized
def test_get_current_user_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 