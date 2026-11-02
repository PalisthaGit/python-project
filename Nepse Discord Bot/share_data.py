import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_percentage(stock):
    return stock['diffPct']


try:
    url = "https://omitnomis.github.io/ShareSansarScraper/api/latest.json"

    response = requests.get(url)
    data = response.json()
    date = data['date']
    stocks = data["rows"]
    total_stocks = data["count"]
    stocks.sort(key=get_percentage, reverse = True)
    top5_stocks = stocks[:5]

    stocks.sort(key=get_percentage, reverse= False)
    top5_losers = stocks[:5]

    message = ""
    message += "📈 NEPSE DAILY HIGHLIGHTS\n\n"
    message += f"Date: {data['date']}\n"
    message += f"Total shares: {data['count']}\n\n"
    message += "TOP 5 GAINERS\n\n"

    for index, top5 in enumerate(top5_stocks, start=1):
        if top5['diffPct'] >0:
            message += f"{index}. {top5['symbol']}: {top5['diffPct']:.2f}%\n"

    message += "\n\nTOP 5 Losers\n\n"

    for index, losers in enumerate(top5_losers, start=1):
            message += f"{index}. {losers['symbol']}: {losers['diffPct']:.2f}%\n"
        
    response=requests.post(os.getenv("WEBHOOK_URL"), json= {"content": message})
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print("Something went wrong!")
        print(response.status_code)

except requests.exceptions.ConnectionError:
    print("Check your internet connection!")



