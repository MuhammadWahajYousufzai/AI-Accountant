"""Tests for expense endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_expenses_unauthorized(client):
    response = await client.get("/api/v1/expenses")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expenses_authorized(client):
    reg = await client.post("/api/v1/auth/register", json={
        "email": "expense-test@example.com",
        "password": "password123",
        "full_name": "Test User",
    })
    if reg.status_code == 409:
        login = await client.post("/api/v1/auth/login", json={
            "email": "expense-test@example.com",
            "password": "password123",
        })
        token = login.json()["access_token"]
    else:
        token = reg.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/expenses", headers=headers)
    assert response.status_code == 200

    create = await client.post("/api/v1/expenses", headers=headers, json={
        "amount_cents": 50000,
        "description": "Test expense",
        "vendor": "Test Vendor",
        "date": "2026-07-28",
        "category_name": "Office Supplies",
    })
    assert create.status_code == 201
    data = create.json()
    assert data["amount_cents"] == 50000
    assert data["description"] == "Test expense"

    expense_id = data["id"]
    get = await client.get(f"/api/v1/expenses/{expense_id}", headers=headers)
    assert get.status_code == 200

    delete = await client.delete(f"/api/v1/expenses/{expense_id}", headers=headers)
    assert delete.status_code == 204
