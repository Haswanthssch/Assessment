"""Tests for Product CRUD endpoints."""


def test_list_products_public(client):
    """Products list is public (no auth required)."""
    res = client.get("/api/v1/products/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_product_as_admin(client, admin_token):
    res = client.post("/api/v1/products/", json={
        "name": "Test Laptop",
        "description": "A test product",
        "price": 999.99,
        "category": "Electronics"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Test Laptop"
    assert data["price"] == 999.99


def test_create_product_non_admin_forbidden(client, user_token):
    res = client.post("/api/v1/products/", json={
        "name": "Sneaky Product",
        "price": 10.0
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 403


def test_get_product(client, admin_token):
    create = client.post("/api/v1/products/", json={
        "name": "Mouse", "price": 25.0, "category": "Electronics"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    pid = create.json()["id"]
    res = client.get(f"/api/v1/products/{pid}")
    assert res.status_code == 200
    assert res.json()["name"] == "Mouse"


def test_update_product_price(client, admin_token):
    create = client.post("/api/v1/products/", json={
        "name": "Keyboard", "price": 50.0
    }, headers={"Authorization": f"Bearer {admin_token}"})
    pid = create.json()["id"]
    res = client.put(f"/api/v1/products/{pid}",
                     json={"price": 75.0},
                     headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["price"] == 75.0


def test_soft_delete_product(client, admin_token):
    create = client.post("/api/v1/products/", json={
        "name": "ToDelete", "price": 1.0
    }, headers={"Authorization": f"Bearer {admin_token}"})
    pid = create.json()["id"]
    res = client.delete(f"/api/v1/products/{pid}",
                        headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    # Confirm product no longer in public list
    check = client.get(f"/api/v1/products/{pid}")
    assert check.status_code == 404
