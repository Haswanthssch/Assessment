"""Tests for User CRUD endpoints."""


def test_register_user(client):
    res = client.post("/api/v1/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "pass123",
        "role": "user"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "alice@test.com"
    assert data["role"] == "user"


def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "username": "bob1", "email": "bob@test.com", "password": "pass123", "role": "user"
    })
    res = client.post("/api/v1/auth/register", json={
        "username": "bob2", "email": "bob@test.com", "password": "pass123", "role": "user"
    })
    assert res.status_code == 400


def test_login_valid(client):
    client.post("/api/v1/auth/register", json={
        "username": "charlie", "email": "charlie@test.com", "password": "pass123", "role": "user"
    })
    res = client.post("/api/v1/auth/login", json={"email": "charlie@test.com", "password": "pass123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_invalid_password(client):
    client.post("/api/v1/auth/register", json={
        "username": "dave", "email": "dave@test.com", "password": "pass123", "role": "user"
    })
    res = client.post("/api/v1/auth/login", json={"email": "dave@test.com", "password": "wrong"})
    assert res.status_code == 401


def test_get_user_as_admin(client, admin_token):
    create = client.post("/api/v1/auth/register", json={
        "username": "eve", "email": "eve@test.com", "password": "pass123", "role": "user"
    })
    uid = create.json()["id"]
    res = client.get(f"/api/v1/users/{uid}", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200


def test_update_user(client, admin_token):
    create = client.post("/api/v1/auth/register", json={
        "username": "frank", "email": "frank@test.com", "password": "pass123", "role": "user"
    })
    uid = create.json()["id"]
    res = client.put(f"/api/v1/users/{uid}",
                     json={"is_active": False},
                     headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["is_active"] is False


def test_delete_user(client, admin_token):
    create = client.post("/api/v1/auth/register", json={
        "username": "grace", "email": "grace@test.com", "password": "pass123", "role": "user"
    })
    uid = create.json()["id"]
    res = client.delete(f"/api/v1/users/{uid}", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
