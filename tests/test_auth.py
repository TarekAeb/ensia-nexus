import pytest
from httpx import AsyncClient

# Mark all async tests in this module to use asyncio
pytestmark = pytest.mark.asyncio

import uuid

@pytest.fixture
def auth_payload():
    return {
        "email": f"test_{uuid.uuid4()}@ensia.edu.dz",
        "password": "Password123!",
        "full_name": "Test Auth User",
        "role": "STUDENT"
    }


async def test_signup_success(client: AsyncClient, auth_payload: dict):
    response = await client.post("/api/v1/auth/signup", json=auth_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == auth_payload["email"]
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_signup_duplicate_email(client: AsyncClient, auth_payload: dict):
    # Register once
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    # Try again
    response = await client.post("/api/v1/auth/signup", json=auth_payload)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


async def test_login_success(client: AsyncClient, auth_payload: dict):
    # First signup
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    # Then login
    login_data = {"email": auth_payload["email"], "password": auth_payload["password"]}
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == auth_payload["email"]
    assert "access_token" in response.cookies


async def test_login_invalid_password(client: AsyncClient, auth_payload: dict):
    # Signup
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    login_data = {"email": auth_payload["email"], "password": "wrongpassword"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401


async def test_get_me(client: AsyncClient, auth_payload: dict):
    # Signup establishes session cookies automatically
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == auth_payload["email"]


async def test_refresh_token(client: AsyncClient, auth_payload: dict):
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    # Hit refresh endpoint which relies on httponly refresh_token cookie
    response = await client.post("/api/v1/auth/refresh")
    assert response.status_code == 200
    # Because cookie-based, httpx handles sending the cookies automatically
    assert "access_token" in response.cookies


async def test_logout(client: AsyncClient, auth_payload: dict):
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    response = await client.delete("/api/v1/auth/logout")
    assert response.status_code == 204
    # The cookies should be empty or expired
    assert "access_token" not in client.cookies or client.cookies.get("access_token") == '""'
