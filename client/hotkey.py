import keyboard
import sys
import os
from capture import take_screenshot
from sender import send_to_server

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

def on_hotkey():
    _log("📸 Делаю скриншот...")
    image_bytes = take_screenshot()
    send_to_server(image_bytes)

def listen_hotkey():
    keyboard.add_hotkey("ctrl+shift+x", on_hotkey)
    _log("Жду нажатия Ctrl+Shift+X. Esc больше не завершает клиент.")
    keyboard.wait()  # ждать любые события, но не выходить на esc
