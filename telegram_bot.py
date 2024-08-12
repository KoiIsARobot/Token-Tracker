import requests
import time
from datetime import datetime
import socks
import socket

telegram_bot_token = '7092830033:AAG0fEOSaFsLua6oSykYkgNDjWjy85YH9uY'
chat_id = '-4210017695'

url = 'https://api.bybit.com/v2/public/symbols'

# Set up the SOCKS5 proxy
socks.set_default_proxy(socks.SOCKS5, "us.922s5.net", 6300, True, "18734042-zone-custom-region-JP-sessid-qqNigu80", "JXUNRlqr")
socket.socket = socks.socksocket

# Function to get data and handle errors
def get_data():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        try:
            return response.json()
        except ValueError:
            print("Failed to decode JSON. Here is the response content:")
            print(response.text)  # Print the raw content if JSON decoding fails
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None

data = get_data()
if data is None:
    print("Exiting script due to failure in getting data.")
    exit()

symbols = []
current_list = []

def telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] — Message sent to Telegram")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] — Failed to send message: {response.text}")


def remove_numbers(input_string):
    for i, char in enumerate(input_string):
        if not char.isdigit():
            return input_string[i:]
    return ""

for el in data["result"]:
    current_list.append(remove_numbers(el["base_currency"]))

print("Initial list of symbols:", current_list)

while True:
    data = get_data()
    if data is None:
        print("Failed to retrieve data, skipping this cycle.")
        time.sleep(5)
        continue

    new_list = []
    new_tokens_found = False

    for el in data["result"]:
        new_list.append(remove_numbers(el["base_currency"]))

    for symbol in new_list:
        if symbol not in current_list:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] —— New token was found — {symbol}")
            current_list.append(symbol)
            new_tokens_found = True
            telegram_message(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] —— New token was found — {symbol}")

    if not new_tokens_found:
        print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] —— No new tokens")

    time.sleep(15)
