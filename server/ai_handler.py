import requests
import os
from prompt_manager import load_prompt

# === API Key ===
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]


def analyze_text(text: str):
    """Send text to Google Gemini API for analysis."""
    system_prompt = load_prompt()

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\n{text}"}
                ],
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        data = res.json()
    except Exception as e:
        return f"GEMINI request failed: {e}"

    if "error" in data:
        return f"GEMINI error: {data['error']}"

    try:
        # Основной ответ Gemini находится здесь
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return content
    except Exception:
        return f"GEMINI response format error: {data}"
