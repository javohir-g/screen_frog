from fastapi import APIRouter, UploadFile, File, HTTPException
import requests
import os
import json
import html
from typing import Optional

router = APIRouter()

LOCAL_SERVER_URL = os.environ.get("LOCAL_SERVER_URL")
if not LOCAL_SERVER_URL:
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            LOCAL_SERVER_URL = cfg.get("local_server_url")
    except Exception:
        LOCAL_SERVER_URL = None

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
if not TELEGRAM_TOKEN or not CHAT_ID:
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
            TELEGRAM_TOKEN = TELEGRAM_TOKEN or cfg.get("telegram_token")
            CHAT_ID = CHAT_ID or cfg.get("chat_id")
    except Exception:
        pass

def tg_send_pre(text: str):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": f"<pre>{html.escape(text)[:3900]}</pre>", "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=15)
    except Exception:
        pass

def tg_send_text(text: str):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, data=data, timeout=15)
    except Exception:
        pass

def tg_send_photo(image_bytes: bytes, caption: Optional[str] = None):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID}
        if caption:
            data["caption"] = caption
        files = {"photo": ("screenshot.png", image_bytes, "image/png")}
        requests.post(url, data=data, files=files, timeout=30)
    except Exception:
        pass

@router.post("/process")
async def proxy_process(file: UploadFile = File(...)):
    if not LOCAL_SERVER_URL:
        raise HTTPException(status_code=500, detail="LOCAL_SERVER_URL not set.")
    try:
        image_bytes = await file.read()
        tg_send_photo(image_bytes, caption="Скриншот")
        files = {"file": (file.filename or "screenshot.png", image_bytes, file.content_type or "image/png")}
        r = requests.post(LOCAL_SERVER_URL, files=files, timeout=60)
        data = r.json() if r.status_code==200 else {}
        ocr_text = data.get("ocr") or data.get("text") or data.get("ocr_text")
        ai_text = data.get("result") or data.get("ai")
        if ocr_text:
            tg_send_pre(ocr_text)
        if ai_text:
            tg_send_text(f"Ответ ИИ:\n{ai_text}")
        return data, r.status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
