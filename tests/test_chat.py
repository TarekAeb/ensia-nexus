import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

import uuid

@pytest.fixture
def auth_payload():
    return {
        "email": f"chat_auth_{uuid.uuid4()}@example.com",
        "password": "Password123!",
        "full_name": "Chat User",
        "role": "STUDENT"
    }


async def test_create_and_get_chat_room(client: AsyncClient, auth_payload: dict):
    # Authenticate
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    # Create room
    room_payload = {
        "name": "General Chat",
        "type": "TEAM"
    }
    response = await client.post("/api/v1/chat/rooms", json=room_payload)
    assert response.status_code == 200
    room_id = response.json().get("id")
    assert room_id is not None
    
    # Get rooms
    list_resp = await client.get("/api/v1/chat/rooms")
    assert list_resp.status_code == 200
    rooms = list_resp.json()
    assert len(rooms) >= 1
    assert any(r["name"] == "General Chat" for r in rooms)


async def test_get_messages_empty(client: AsyncClient, auth_payload: dict):
    await client.post("/api/v1/auth/signup", json=auth_payload)
    
    room_payload = {
        "name": "Empty Chat",
        "type": "TEAM"
    }
    room_resp = await client.post("/api/v1/chat/rooms", json=room_payload)
    room_id = room_resp.json()["id"]
    
    msg_resp = await client.get(f"/api/v1/chat/rooms/{room_id}/messages")
    assert msg_resp.status_code == 200
    assert msg_resp.json() == []


# In FastAPI, testing websockets requires a specific test client using Context Managers
# which isn't cleanly supported by async httpx without a special Websocket client, 
# but we can rely on standard unit tests to mock Manager if needed, or ignore ws tests for now.
