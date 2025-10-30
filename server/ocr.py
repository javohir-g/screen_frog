from PIL import Image
import pytesseract
import io
import os
import shutil

def _configure_tesseract_path():
    # 1) If tesseract is on PATH
    which_path = shutil.which("tesseract")
    if which_path:
        pytesseract.pytesseract.tesseract_cmd = which_path
        return

    # 2) If provided via env var
    env_path = os.environ.get("TESSERACT_PATH")
    if env_path and os.path.exists(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return

    # 3) Common Windows install locations
    candidates = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        r"D:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        r"Tesseract-OCR\\tesseract.exe",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            return

    # Leave default; pytesseract will raise a helpful error at runtime
    pass

_configure_tesseract_path()

def extract_text(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang="eng+rus")
    print("🧾 Распознанный текст:", text[:100])
    return text
