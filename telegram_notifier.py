import requests
import json
import sys

TOKEN = '8339422193:AAFVgrrIPAeXhtOoZ-l-oapZaigm7100ilk'

def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok") and len(response["result"]) > 0:
            # Get the chat ID of the most recent message sent to the bot
            return response["result"][-1]["message"]["chat"]["id"]
    except Exception as e:
        print(f"Error getting updates: {e}")
    return None

def send_message(text, chat_id=None):
    if not chat_id:
        chat_id = get_chat_id()
        
    if not chat_id:
        print("Could not find a Chat ID. Please send a message to your Telegram bot first.")
        return False
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram message sent successfully.")
            return True
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")
        
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
        send_message(message)
    else:
        print("Usage: python telegram_notifier.py 'Your message here'")
