import requests
import os
from dotenv import load_dotenv

load_dotenv()
message = input("Enter the message you want to send: ")
try:

    response=requests.post(os.getenv("WEBHOOK_URL"), json= {"content": message})
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print("Something went wrong!")

except requests.exceptions.ConnectionError:
    print("Check your internet connection!")