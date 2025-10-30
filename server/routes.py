from fastapi import APIRouter, UploadFile, File, HTTPException
from ocr import extract_text
from ai_handler import analyze_text
from telegram_bot import send_to_telegram, send_photo, send_pre
import traceback
import uuid

router = APIRouter()

@router.get("/")
async def root():
    return {"status": "ok", "message": "Screen Frog server is running"}

@router.get("/healthz")
async def healthz():
    return {"ok": True}

@router.post("/process")
async def process(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        # 1) Сначала отправляем скриншот
        try:
            send_photo(image_data, caption="Скриншот")
        except Exception as e:
            print(f"⚠️ Ошибка отправки фото в Telegram: {e}")

        # 2) Затем отправляем распознанный текст
        text = extract_text(image_data)
        try:
            send_pre(text[:3900])
        except Exception as e:
            print(f"⚠️ Ошибка отправки текста в Telegram: {e}")

        # 3) И потом ответ ИИ
        result = analyze_text(text)
        try:
            send_to_telegram(result)
        except Exception as e:
            print(f"⚠️ Ошибка отправки ответа ИИ в Telegram: {e}")
        return {"status": "ok", "ocr": text, "result": result}
    except Exception as e:
        error_msg = f"Internal error: {str(e)}"
        print(f"❌ Ошибка обработки: {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)
