from hotkey import listen_hotkey
import sys
import os

def main():
    # Общая стабилизация: по возможности минимизируем использование COM.
    # Для проблемных окружений можно полностью отключить dxcam:
    # set SCREENFROG_NO_DXCAM=1
    # For compiled exe, try to write to log file in exe directory
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        log_path = os.path.join(exe_dir, "client.log")
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("🚀 Клиент запущен. Нажми Ctrl+Shift+X для скриншота.\n")
        except:
            pass
    else:
        print("🚀 Клиент запущен. Нажми Ctrl+Shift+X для скриншота. Esc — выход.")
    
    try:
        listen_hotkey()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            log_path = os.path.join(exe_dir, "client.log")
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"❌ Ошибка: {e}\n")
            except:
                pass
        raise

if __name__ == "__main__":
    main()
