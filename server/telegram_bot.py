import requests
import json
import html

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def send_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendMessage"
    data = {"chat_id": CONFIG["chat_id"], "text": text}
    requests.post(url, data=data)

def send_pre(text: str):
    url = f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendMessage"
    escaped = html.escape(text)
    data = {
        "chat_id": CONFIG["chat_id"],
        "text": f"<pre>{escaped}</pre>",
        "parse_mode": "HTML",
    }
    requests.post(url, data=data)

def send_photo(image_bytes: bytes, caption: str | None = None):
    url = f"https://api.telegram.org/bot{CONFIG['telegram_token']}/sendPhoto"
    data = {"chat_id": CONFIG["chat_id"]}
    if caption:
        data["caption"] = caption
    files = {"photo": ("screenshot.png", image_bytes, "image/png")}
    requests.post(url, data=data, files=files)
