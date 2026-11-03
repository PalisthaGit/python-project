import pytest
from fastapi.testclient import TestClient
from api import app, get_db_path
from db import create_prices_table, save_prices


def make_stock(symbol, close):
    return {"symbol": symbol, "open": close, "high": close, "low": close,
            "close": close, "vol": 100}


@pytest.fixture
def client(tmp_path):
    path = str(tmp_path / "test.db")
    create_prices_table(path)
    save_prices("2026-10-26", [make_stock("NABIL", 100), make_stock("ACLBSL", 200)], path)
    save_prices("2026-11-02", [make_stock("NABIL", 110), make_stock("ACLBSL", 180)], path)
    app.dependency_overrides[get_db_path] = lambda: path
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def empty_client(tmp_path):
    path = str(tmp_path / "empty.db")
    create_prices_table(path)
    app.dependency_overrides[get_db_path] = lambda: path
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_latest_prices(client):
    response = client.get("/prices/latest")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == "2026-11-02"
    assert body["count"] == 2


def test_latest_prices_empty_database(empty_client):
    assert empty_client.get("/prices/latest").status_code == 404


def test_price_history(client):
    response = client.get("/prices/NABIL?days=30")
    assert response.status_code == 200
    history = response.json()["history"]
    assert [row["date"] for row in history] == ["2026-10-26", "2026-11-02"]


def test_price_history_accepts_lowercase_symbol(client):
    assert client.get("/prices/nabil").status_code == 200


def test_price_history_unknown_symbol(client):
    assert client.get("/prices/FAKE").status_code == 404


def test_price_history_rejects_bad_days(client):
    assert client.get("/prices/NABIL?days=0").status_code == 422
    assert client.get("/prices/NABIL?days=9999").status_code == 422


def test_weekly_movers(client):
    response = client.get("/weekly-movers?limit=1")
    assert response.status_code == 200
    body = response.json()
    assert body["gainers"] == [{"symbol": "NABIL", "change_pct": 10.0}]
    assert body["losers"] == [{"symbol": "ACLBSL", "change_pct": -10.0}]


def test_weekly_movers_not_enough_history(empty_client):
    assert empty_client.get("/weekly-movers").status_code == 404