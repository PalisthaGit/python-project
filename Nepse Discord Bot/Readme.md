# NEPSE Stock Tracker

A Python project that saves daily NEPSE share prices in a SQLite database, sends a daily summary to Discord, and serves the saved data through a REST API built with FastAPI.

## Features
- Fetches the latest NEPSE data from a public JSON source
- Saves each day's prices in SQLite (the same share on the same date is never saved twice)
- Sends the daily top 5 gainers and losers, plus weekly movers, to Discord through a webhook
- Runs automatically every day with a scheduled GitHub Actions workflow
- REST API for latest prices, price history of one share, and weekly gainers and losers
- Input validation and clear error responses
- Automated tests with pytest, run on every push with GitHub Actions

## Tech
Python, FastAPI, SQLite, SQL, pytest, requests, Discord webhooks, GitHub Actions

## API endpoints

| Endpoint | What it returns |
|---|---|
| `GET /health` | `{"status": "ok"}` |
| `GET /prices/latest` | All prices for the newest saved day |
| `GET /prices/{symbol}?days=30` | Price history of one share (days from 1 to 365) |
| `GET /weekly-movers?limit=5` | Top gainers and losers over the last 7 days |

Errors: `404` for an unknown share or missing data, `422` for invalid parameters.
FastAPI also creates interactive docs at `/docs`.

Example:
```
GET /prices/NABIL?days=7
```

## Setup
1. Clone the repo and open the `Nepse Discord Bot` folder.
2. Run `pip install -r requirements-dev.txt`.
3. Create a `.env` file with `WEBHOOK_URL=your_discord_webhook_url`.
4. Run `python3 share_data.py` to save today's prices and send the Discord message.
5. Start the API with `uvicorn api:app --reload` and open `http://127.0.0.1:8000/docs`.

## Tests
```
python3 -m pytest
```

## Notes
- The weekly movers need at least 7 days of saved data, so they appear after the bot has run for a week.
- The database file is committed back to the repo by the daily workflow.

## How this project was built
I built this project with AI assistance (Claude) while learning Python, SQL, FastAPI and testing. I review every part of the code to understand it, and I am writing more tests myself as I learn.

## Planned
- Deploy the API online
- More tests for failure cases (data source down, bad data)