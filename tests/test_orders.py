"""Integration tests: Order flow → SQL + (mock) MongoDB log."""
from unittest.mock import patch


def _create_product(client, admin_token, price=50.0):
    res = client.post("/api/v1/products/", json={
        "name": f"Product-{price}", "price": price, "category": "Test"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 201
    return res.json()


@patch("src.services.log_service.activity_logs_col")
@patch("src.services.log_service.order_history_col")
def test_create_order_integration(mock_order_col, mock_activity_col, client, admin_token, user_token):
    """
    Integration test: create product → user places order →
    verify SQL record created + MongoDB log was triggered.
    """
    # Setup mock MongoDB collections
    mock_activity_col.insert_one.return_value = None
    mock_order_col.insert_one.return_value = None

    # Create product as admin
    product = _create_product(client, admin_token, price=100.0)
    pid = product["id"]

    # Update inventory (set qty to 20)
    client.put(f"/api/v1/inventory/{pid}",
               json={"quantity": 20, "reorder_level": 5},
               headers={"Authorization": f"Bearer {admin_token}"})

    # Place order as user
    res = client.post("/api/v1/orders/", json={
        "shipping_address": "123 Test Street, Chennai",
        "items": [{"product_id": pid, "quantity": 2, "unit_price": 100.0}]
    }, headers={"Authorization": f"Bearer {user_token}"})

    assert res.status_code == 201
    order = res.json()
    assert order["total_amount"] == 200.0
    assert order["status"] == "pending"
    assert len(order["items"]) == 1

    # Verify MongoDB log was called
    assert mock_order_col.insert_one.called


def test_list_orders_as_admin(client, admin_token):
    res = client.get("/api/v1/orders/", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@patch("src.services.log_service.order_history_col")
def test_update_order_status(mock_col, client, admin_token, user_token):
    mock_col.insert_one.return_value = None

    product = _create_product(client, admin_token, price=30.0)
    pid = product["id"]
    client.put(f"/api/v1/inventory/{pid}",
               json={"quantity": 10, "reorder_level": 2},
               headers={"Authorization": f"Bearer {admin_token}"})

    order_res = client.post("/api/v1/orders/", json={
        "shipping_address": "456 Test Ave",
        "items": [{"product_id": pid, "quantity": 1, "unit_price": 30.0}]
    }, headers={"Authorization": f"Bearer {user_token}"})
    oid = order_res.json()["id"]

    # Admin updates status
    status_res = client.put(f"/api/v1/orders/{oid}/status",
                            json={"status": "confirmed"},
                            headers={"Authorization": f"Bearer {admin_token}"})
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "confirmed"


def test_insufficient_stock_rejected(client, admin_token, user_token):
    product = _create_product(client, admin_token, price=200.0)
    pid = product["id"]
    # Set qty to 0
    client.put(f"/api/v1/inventory/{pid}",
               json={"quantity": 0, "reorder_level": 5},
               headers={"Authorization": f"Bearer {admin_token}"})

    res = client.post("/api/v1/orders/", json={
        "shipping_address": "789 Test Blvd",
        "items": [{"product_id": pid, "quantity": 5, "unit_price": 200.0}]
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 400
