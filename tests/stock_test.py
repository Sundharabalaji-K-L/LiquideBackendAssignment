from http.client import responses

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user


def raise_unauthorized():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated")


@pytest.mark.parametrize("endpoint", [

    "/stock/holdings",
    "/stock/positions",
    "/stock/orders"
])
def test_unauthorized_access(client: TestClient, endpoint: str):
    app.dependency_overrides[get_current_user] = raise_unauthorized

    response = client.get(endpoint)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    app.dependency_overrides.clear()


def test_get_holdings_authenticated(authorized_client):
    response = authorized_client.get("/stock/holdings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    assert len(data) == 2
    assert data[0]["symbol"] == "AAPL"
    assert data[0]["quantity"] == 15
    assert data[1]["symbol"] == "GOOGL"
    assert data[1]["quantity"] == 5


def test_get_positions_authenticated(authorized_client):
    response = authorized_client.get("/stock/positions")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]["symbol"] == "TSLA"


def test_get_orders_authenticated(authorized_client):
    response = authorized_client.get("/stock/orders")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]["symbol"] == "MSFT"
    assert data[0]["status"] == "executed"