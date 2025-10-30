import requests
import json
import os
import sys

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

def send_to_server(image_bytes):
    try:
        response = requests.post(
            CONFIG["server_url"],
            files={"file": ("screenshot.png", image_bytes, "image/png")},
            timeout=30
        )
        _log(f"✅ Ответ от сервера: {response.text}")
    except Exception as e:
        _log(f"❌ Ошибка отправки: {e}")
