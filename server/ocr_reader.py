# OCR реализован через Google Vision API
import os
import io
from typing import Optional

from PIL import Image

try:
    # Lazy import to keep import errors informative
    from google.cloud import vision
except Exception:  # pragma: no cover
    vision = None


GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or "google_vision_key.json"


def _ensure_credentials() -> Optional[str]:
    """Ensure GOOGLE_APPLICATION_CREDENTIALS is set to an existing json file.

    Returns the path if available, otherwise prints an instruction and returns None.
    """
    # Allow overriding via env, otherwise set default
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH

    cred_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    if not os.path.exists(cred_path):
        print(
            "⚠️ Файл google_vision_key.json не найден.\n"
            "Получите JSON ключ сервисного аккаунта в Google Cloud Console → IAM & Admin → Service Accounts → Keys,\n"
            "затем сохраните его рядом с приложением как 'google_vision_key.json' или укажите путь в переменной окружения GOOGLE_APPLICATION_CREDENTIALS."
        )
        return None
    return cred_path


def _build_client() -> "vision.ImageAnnotatorClient":
    if vision is None:
        raise RuntimeError(
            "Пакет google-cloud-vision не установлен. Установите: pip install google-cloud-vision pillow"
        )
    cred_ok = _ensure_credentials()
    if not cred_ok:
        raise FileNotFoundError("Файл с ключом Google Vision не найден.")
    return vision.ImageAnnotatorClient()


def extract_text(image_bytes: bytes) -> str:
    """Run OCR using Google Vision API and return extracted text as str."""
    # Validate image is loadable (gives clearer errors than API when bytes are wrong)
    try:
        Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        raise ValueError(f"Невозможно открыть изображение: {e}")

    try:
        client = _build_client()
        image = vision.Image(content=image_bytes)
        # document_text_detection gives better layout-aware text for UI screenshots
        response = client.document_text_detection(image=image)

        if response.error and response.error.message:
            raise RuntimeError(f"Google Vision API error: {response.error.message}")

        annotation = response.full_text_annotation
        text = annotation.text if annotation and annotation.text else ""

        if not text:
            # Fallback to standard text_detection
            alt = client.text_detection(image=image)
            if alt.error and alt.error.message:
                raise RuntimeError(f"Google Vision API error: {alt.error.message}")
            if alt.text_annotations:
                text = alt.text_annotations[0].description or ""

        text = (text or "").strip()
        if not text:
            return ""  # explicitly return empty string when no text found
        print("🧾 Распознанный текст:", text[:100])
        return text
    except Exception as e:
        # Provide concise, actionable error for callers
        raise RuntimeError(f"Ошибка OCR (Google Vision): {e}")


