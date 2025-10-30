FROM python:3.12-slim

# 1. Базовые утилиты и обновление pip
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# 2. Копируем server/
WORKDIR /app
COPY . /app

# 3. Установка всех python-зависимостей
RUN pip install -r requirements.txt

# 4. Экспонируем порт (по умолчанию FastAPI 8000)
EXPOSE 8000

# 5. Старт
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
