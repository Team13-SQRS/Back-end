import pytest
from fastapi import status
from app.database.models import Note


# Fixture to provide auth headers for a logged-in user
@pytest.fixture
def auth_headers(client, test_user):
    login_response = client.post(
        "/auth/login", json={"username": "testuser", "password": "testpass"}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# Fixture to create a test note in the database
@pytest.fixture
def test_note(db, test_user):
    note = Note(user_id=test_user.id, title="Test Note", content="Test Content")
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# Test creating a note with valid authentication
def test_create_note_success(client, auth_headers):
    response = client.post(
        "/api/notes/",
        json={"title": "New Note", "content": "New Content"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New Note"
    assert data["content"] == "New Content"


# Test creating a note without authentication returns unauthorized
def test_create_note_unauthorized(client):
    response = client.post(
        "/api/notes/", json={"title": "New Note", "content": "New Content"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Test retrieving a note by ID with valid authentication
def test_get_note_success(client, auth_headers, test_note):
    response = client.get(f"/api/notes/{test_note.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"


# Test retrieving a non-existent note returns not found
def test_get_note_not_found(client, auth_headers):
    response = client.get("/api/notes/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Test updating a note with valid authentication
def test_update_note_success(client, auth_headers, test_note):
    response = client.put(
        f"/api/notes/{test_note.id}",
        json={"title": "Updated Note", "content": "Updated Content"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Note"
    assert data["content"] == "Updated Content"


# Test deleting a note with valid authentication
def test_delete_note_success(client, auth_headers, test_note):
    response = client.delete(f"/api/notes/{test_note.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK


# Test listing notes for a user with valid authentication
def test_list_notes_success(client, auth_headers, test_note):
    response = client.get("/api/notes/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Note"


# Test translating a note with valid authentication
def test_translate_note_success(client, auth_headers, test_note):
    response = client.post(
        f"/api/notes/{test_note.id}/translate",
        json={"target_lang": "en"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "translated_text" in data
