import sqlite3
import pytest
from db import create_prices_table, save_prices, get_weekly_changes, normalize_date
from share_data import build_daily_message, build_weekly_message


def make_stock(symbol, close, diff_pct=0):
    return {"symbol": symbol, "open": close, "high": close, "low": close,
            "close": close, "vol": 100, "diffPct": diff_pct}


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    create_prices_table(path)
    return path


def test_normalize_date():
    assert normalize_date("2026-11-02") == "2026-11-02"
    assert normalize_date("02/11/2026") == "2026-11-02"


def test_normalize_date_unknown_format():
    with pytest.raises(ValueError):
        normalize_date("not a date")


def test_save_prices_does_not_duplicate(db_path):
    stocks = [make_stock("NABIL", 500), make_stock("ACLBSL", 850)]
    save_prices("2026-11-02", stocks, db_path)
    save_prices("2026-11-02", stocks, db_path)  # same day again

    connection = sqlite3.connect(db_path)
    count = connection.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    connection.close()
    assert count == 2


def test_weekly_changes(db_path):
    save_prices("2026-10-26", [make_stock("NABIL", 100), make_stock("ACLBSL", 200)], db_path)
    save_prices("2026-11-02", [make_stock("NABIL", 110), make_stock("ACLBSL", 180)], db_path)

    changes = get_weekly_changes("2026-11-02", db_path)
    assert changes == [("NABIL", 10.0), ("ACLBSL", -10.0)]


def test_weekly_changes_not_enough_history(db_path):
    save_prices("2026-11-02", [make_stock("NABIL", 110)], db_path)
    assert get_weekly_changes("2026-11-02", db_path) == []


def test_daily_message_has_gainers_and_losers():
    stocks = [make_stock("UP", 100, 5.0), make_stock("DOWN", 100, -3.0)]
    message = build_daily_message("2026-11-02", 2, stocks)
    assert "UP: 5.00%" in message
    assert "DOWN: -3.00%" in message


def test_weekly_message_when_no_history():
    assert "7 days" in build_weekly_message([])