from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from db import (
    DB_PATH,
    create_prices_table,
    get_latest_date,
    get_prices_for_date,
    get_symbol_history,
    get_weekly_changes,
)


@asynccontextmanager
async def lifespan(app):
    create_prices_table()  # make sure the table exists when the API starts
    yield


app = FastAPI(
    title="NEPSE Stock Tracker API",
    description="Serves the NEPSE prices saved by the daily bot.",
    lifespan=lifespan,
)


def get_db_path():
    """The database file. Tests replace this with a temporary database."""
    return DB_PATH


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/prices/latest")
def latest_prices(db_path: str = Depends(get_db_path)):
    date = get_latest_date(db_path)
    if date is None:
        raise HTTPException(status_code=404, detail="No prices saved yet.")
    prices = get_prices_for_date(date, db_path)
    return {"date": date, "count": len(prices), "prices": prices}


@app.get("/prices/{symbol}")
def price_history(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="How many days back to show"),
    db_path: str = Depends(get_db_path),
):
    symbol = symbol.upper()
    history = get_symbol_history(symbol, days, db_path)
    if not history:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}.")
    return {"symbol": symbol, "days": days, "history": history}


@app.get("/weekly-movers")
def weekly_movers(
    limit: int = Query(5, ge=1, le=20),
    db_path: str = Depends(get_db_path),
):
    date = get_latest_date(db_path)
    changes = get_weekly_changes(date, db_path) if date else []
    if not changes:
        raise HTTPException(status_code=404, detail="Not enough history yet (needs 7 days of data).")

    gainers = [{"symbol": s, "change_pct": pct} for s, pct in changes[:limit]]
    losers = [{"symbol": s, "change_pct": pct} for s, pct in reversed(changes[-limit:])]
    return {"date": date, "gainers": gainers, "losers": losers}