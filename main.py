from datetime import datetime
import os
import time
import requests

# Replace these with your bot's API token and your chat ID
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
TG_ADMIN_ID = os.getenv('TG_ADMIN_ID')
if not BOT_API_TOKEN or not TG_ADMIN_ID:
    raise Exception("no env vars")
MESSAGE = 'Hello, Denis! This is a test message from your bot.'

def send_raw_telegram_message(bot_token, chat_id, message) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def get_raw_updates(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        print(updates)
    else:
        print(f"Failed to get updates. Status code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    get_raw_updates(BOT_API_TOKEN)
    send_raw_telegram_message(
        BOT_API_TOKEN, 
        TG_ADMIN_ID, 
        f"Hello! Main program has started, server time is: {datetime.now().isoformat()}"
    )
    time.sleep(60)

