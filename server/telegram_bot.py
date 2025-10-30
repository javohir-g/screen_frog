import requests
import json
import html
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def send_pre(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    escaped = html.escape(text)
    data = {
        "chat_id": CHAT_ID,
        "text": f"<pre>{escaped}</pre>",
        "parse_mode": "HTML",
    }
    requests.post(url, data=data)

def send_photo(image_bytes: bytes, caption: str | None = None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    data = {"chat_id": CHAT_ID}
    if caption:
        data["caption"] = caption
    files = {"photo": ("screenshot.png", image_bytes, "image/png")}
    requests.post(url, data=data, files=files)
