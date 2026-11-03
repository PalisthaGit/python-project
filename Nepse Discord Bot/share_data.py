import os
import requests
from dotenv import load_dotenv
from db import create_prices_table, save_prices, get_weekly_changes, normalize_date

load_dotenv()

URL = "https://omitnomis.github.io/ShareSansarScraper/api/latest.json"


def get_percentage(stock):
    return stock["diffPct"]


def build_daily_message(date, total_stocks, stocks):
    top5_gainers = sorted(stocks, key=get_percentage, reverse=True)[:5]
    top5_losers = sorted(stocks, key=get_percentage)[:5]

    message = "📈 NEPSE DAILY HIGHLIGHTS\n\n"
    message += f"Date: {date}\n"
    message += f"Total shares: {total_stocks}\n\n"
    message += "TOP 5 GAINERS\n\n"
    for index, stock in enumerate(top5_gainers, start=1):
        if stock["diffPct"] > 0:
            message += f"{index}. {stock['symbol']}: {stock['diffPct']:.2f}%\n"

    message += "\n\nTOP 5 LOSERS\n\n"
    for index, stock in enumerate(top5_losers, start=1):
        message += f"{index}. {stock['symbol']}: {stock['diffPct']:.2f}%\n"
    return message


def build_weekly_message(changes):
    if not changes:
        return "\n\n📅 Weekly movers will appear once 7 days of data are saved."

    message = "\n\n📅 WEEKLY TOP 5 GAINERS\n\n"
    for index, (symbol, pct) in enumerate(changes[:5], start=1):
        message += f"{index}. {symbol}: {pct:.2f}%\n"

    message += "\n\n📅 WEEKLY TOP 5 LOSERS\n\n"
    for index, (symbol, pct) in enumerate(reversed(changes[-5:]), start=1):
        message += f"{index}. {symbol}: {pct:.2f}%\n"
    return message


def send_to_discord(message):
    response = requests.post(os.getenv("WEBHOOK_URL"), json={"content": message})
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print("Something went wrong!")
        print(response.status_code)


def main():
    try:
        response = requests.get(URL, timeout=30)
        data = response.json()
    except requests.exceptions.RequestException:
        print("Could not get the NEPSE data. Check your internet connection or the data source.")
        return

    date = normalize_date(data["date"])
    stocks = data["rows"]

    create_prices_table()
    save_prices(date, stocks)

    message = build_daily_message(date, data["count"], stocks)
    message += build_weekly_message(get_weekly_changes(date))
    send_to_discord(message)


if __name__ == "__main__":
    main()