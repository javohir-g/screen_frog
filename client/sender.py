import requests
import json
import os
import sys
import io
from typing import Optional, Tuple
from PIL import Image

def _get_config_path():
    if getattr(sys, 'frozen', False):
        # If running as compiled exe, look for config.json next to exe
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, "config.json")
    else:
        # If running as script, look in current directory
        return os.path.join(os.path.dirname(__file__), "config.json")

try:
    config_path = _get_config_path()
    with open(config_path, "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"config.json not found at {config_path}. Please place config.json next to the executable.")

def _log(message):
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        log_path = os.path.join(exe_dir, "client.log")
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
        except:
            pass
    else:
        print(message)

def _reencode(image_bytes: bytes, max_side: int, quality: int) -> bytes:
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        scale = min(1.0, float(max_side) / max(w, h))
        if scale < 1.0:
            img = img.resize((int(w * scale), int(h * scale)))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()
    except Exception:
        return image_bytes


def _wake_server_if_needed(url: str, timeout_s: int):
    try:
        # Try to call docs endpoint to wake Render dyno
        base = url.rsplit("/", 1)[0]
        docs = base + "/docs"
        requests.get(docs, timeout=timeout_s)
    except Exception:
        pass


def send_to_server(image_bytes):
    server_url = CONFIG.get("server_url")
    timeout_s = int(CONFIG.get("timeout_s", 60))

    _wake_server_if_needed(server_url, min(10, timeout_s))

    attempts = [
        (image_bytes, "image/png", None),           # original PNG
        (_reencode(image_bytes, 1600, 80), "image/jpeg", (1600, 80)),
        (_reencode(image_bytes, 1200, 70), "image/jpeg", (1200, 70)),
    ]

    last_error: Optional[Exception] = None
    for idx, (payload, mime, hint) in enumerate(attempts, start=1):
        try:
            response = requests.post(
                server_url,
                files={"file": ("screenshot.jpg" if mime=="image/jpeg" else "screenshot.png", payload, mime)},
                timeout=timeout_s
            )
            _log(f"✅ Ответ от сервера: {response.text}")
            return
        except Exception as e:
            last_error = e
            if hint:
                size_hint = f" (fallback {hint[0]}px q{hint[1]})"
            else:
                size_hint = ""
            _log(f"⚠️ Ошибка отправки, попытка {idx}/{len(attempts)}{size_hint}: {e}")
    _log(f"❌ Ошибка отправки: {last_error}")
