"""Tests for MongoDB activity log endpoints."""
from unittest.mock import patch


@patch("src.services.log_service.activity_logs_col")
def test_activity_log_insert_on_login(mock_col, client):
    """Verify MongoDB insert is called when user logs in."""
    mock_col.insert_one.return_value = None

    client.post("/api/v1/auth/register", json={
        "username": "logtest", "email": "logtest@test.com",
        "password": "pass123", "role": "user"
    })
    login_res = client.post("/api/v1/auth/login", json={
        "email": "logtest@test.com", "password": "pass123"
    })
    assert login_res.status_code == 200
    assert mock_col.insert_one.called


@patch("src.routes.logs.get_activity_logs")
def test_admin_can_fetch_logs(mock_get_logs, client, admin_token):
    """Admin can fetch activity logs."""
    mock_get_logs.return_value = [
        {"_id": "abc123", "user_id": 1, "username": "admin",
         "action": "login", "timestamp": "2024-01-01T00:00:00"}
    ]
    res = client.get("/api/v1/logs/activity", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 1
    assert data["logs"][0]["action"] == "login"


@patch("src.routes.logs.get_activity_logs")
def test_non_admin_cannot_fetch_logs(mock_get_logs, client, user_token):
    """Regular users cannot access logs."""
    res = client.get("/api/v1/logs/activity", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 403


@patch("src.routes.logs.get_order_history")
def test_order_history_fetch(mock_get_history, client, admin_token):
    """Admin can fetch order status history from MongoDB."""
    mock_get_history.return_value = [
        {"_id": "xyz789", "order_id": 1, "old_status": "pending",
         "new_status": "confirmed", "timestamp": "2024-01-01T00:00:00"}
    ]
    res = client.get("/api/v1/logs/order-history", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["history"][0]["new_status"] == "confirmed"
