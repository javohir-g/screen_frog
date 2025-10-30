## Screen Frog

Инструмент для быстрого захвата скриншотов на Windows и их анализа ИИ через сервер на FastAPI. Клиент по горячей клавише делает скриншот, отправляет его на сервер, сервер распознаёт текст (Tesseract OCR), анализирует и отправляет результаты в Telegram.

### Возможности
- Захват экрана горячей клавишей `Ctrl+Shift+X`
- Отправка скриншота на сервер одним действием
- OCR через Tesseract (английский и русский языки)
- Анализ текста ИИ (подключение через сервер)
- Уведомления в Telegram: изображение, распознанный текст, ответ ИИ

### Архитектура
- `client/`: Windows-клиент (Python → PyInstaller .exe)
  - `capture.py` — захват экрана
  - `hotkey.py` — глобальная горячая клавиша
  - `sender.py` — отправка на сервер
  - `main.py` — входная точка клиента
- `server/`: FastAPI-сервер
  - `routes.py` — эндпоинт `/process`
  - `ocr.py` — OCR через Tesseract
  - `ai_handler.py` — анализ текста ИИ
  - `telegram_bot.py` — отправка в Telegram

### Требования
- Клиент: Windows 10/11
- Сервер: Python 3.11/3.12, установленный Tesseract-OCR (eng + rus)

### Установка сервера (локально)
```powershell
cd server
python -m pip install -r requirements.txt
# Установите Tesseract-OCR (включая рус/eng языки)
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Сборка клиента (.exe)
```powershell
cd client
build.bat
# Готовый файл: client/dist/ScreenAI-Client.exe
```

Рядом с `.exe` положите `config.json`:
```json
{
  "server_url": "http://<SERVER_IP>:8000/process"
}
```

### Использование
1. Запустите сервер (`uvicorn ...`)
2. Запустите клиент `ScreenAI-Client.exe`
3. Нажмите `Ctrl+Shift+X` — скриншот отправится на сервер
4. Проверьте Telegram-чат: придут картинка, распознанный текст и ответ ИИ

### Настройка Tesseract (Windows)
- Установите Tesseract-OCR (официальный установщик)
- Убедитесь, что `tesseract.exe` доступен в PATH или задайте `TESSERACT_PATH` в переменных окружения

### Полезное
- Логи клиента пишутся в `client.log` рядом с `.exe`
- Серверные зависимости: см. `server/requirements.txt`
- Для Docker-окружения используйте `server/Dockerfile` (устанавливает Tesseract в образ)

### Лицензия
MIT (при необходимости обновите по требованиям проекта)
