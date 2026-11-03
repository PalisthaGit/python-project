import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "nepse.db")


def normalize_date(text):
    """Turn the date from the data into YYYY-MM-DD so dates can be compared."""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unknown date format: {text}")


def create_prices_table(db_path=DB_PATH):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS prices (
            date TEXT NOT NULL,
            symbol TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            PRIMARY KEY (date, symbol)
        )""")
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while creating the prices table: {e}")
    finally:
        if connection:
            connection.close()


def save_prices(date, stocks, db_path=DB_PATH):
    rows = []
    for stock in stocks:
        rows.append((
            date,
            stock["symbol"],
            stock["open"],
            stock["high"],
            stock["low"],
            stock["close"],
            stock["vol"],
        ))

    connection = None
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO prices (date, symbol, open, high, low, close, volume) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while saving prices: {e}")
    finally:
        if connection:
            connection.close()


def get_weekly_changes(latest_date, db_path=DB_PATH):
    """Return [(symbol, weekly_change_pct), ...] sorted from highest to lowest.
    Returns an empty list if there is not 7 days of history yet."""
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # the newest saved day that is at least 7 days before the latest day
        cursor.execute(
            "SELECT MAX(date) FROM prices WHERE date <= date(?, '-7 days')",
            (latest_date,),
        )
        base_date = cursor.fetchone()[0]
        if base_date is None:
            return []

        cursor.execute(
            """SELECT t.symbol,
                      ROUND((t.close - b.close) * 100.0 / b.close, 2) AS change_pct
               FROM prices t
               JOIN prices b ON t.symbol = b.symbol
               WHERE t.date = ? AND b.date = ? AND b.close > 0
               ORDER BY change_pct DESC""",
            (latest_date, base_date),
        )
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while reading weekly changes: {e}")
        return []
    finally:
        if connection:
            connection.close()


def _query(sql, params=(), db_path=DB_PATH):
    """Run a SELECT and return the rows as a list of dictionaries."""
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"An error occurred while reading data: {e}")
        return []
    finally:
        if connection:
            connection.close()


def get_latest_date(db_path=DB_PATH):
    rows = _query("SELECT MAX(date) AS latest FROM prices", (), db_path)
    return rows[0]["latest"] if rows else None


def get_prices_for_date(date, db_path=DB_PATH):
    return _query(
        "SELECT symbol, open, high, low, close, volume FROM prices "
        "WHERE date = ? ORDER BY symbol",
        (date,),
        db_path,
    )


def get_symbol_history(symbol, days, db_path=DB_PATH):
    """Prices of one share for the last `days` days (counted back from the newest saved day)."""
    return _query(
        "SELECT date, open, high, low, close, volume FROM prices "
        "WHERE symbol = ? AND date >= date((SELECT MAX(date) FROM prices), ?) "
        "ORDER BY date",
        (symbol, f"-{days} days"),
        db_path,
    )