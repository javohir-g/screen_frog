import requests
import os
from prompt_manager import load_prompt

OPENAI_KEY = os.environ["OPENAI_KEY"]
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def analyze_text(text: str):
    system_prompt = load_prompt()
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "max_tokens": 400,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    try:
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        data = res.json()
    except Exception as e:
        return f"AI request failed: {e}"

    if res.status_code != 200:
        err = (data.get("error") or {}).get("message") if isinstance(data, dict) else None
        return f"AI error: HTTP {res.status_code} | {err or data}"

    choices = data.get("choices")
    if not choices:
        return f"AI response missing choices: {data}"
    message = choices[0].get("message", {})
    content = message.get("content")
    if not content:
        return f"AI response missing content: {data}"
    return content


