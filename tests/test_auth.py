import pytest
from fastapi import status


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testeruser",
            "email": "tester@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testeruser"
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert "password" not in data


def test_create_duplicate_user(client):
    # Create first user
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )

    # Try to create user with same email
    response = client.post(
        "/users/",
        json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client):
    # Create user first
    client.post(
        "/users/",
        json={
            "username": "testeruser",
            "email": "tester@example.com",
            "password": "testpassword",
        },
    )

    # Try to login
    response = client.post(
        "/auth/login", json={"username": "testeruser", "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    # Create user first
    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )

    # Try to login with wrong password
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login", json={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]
