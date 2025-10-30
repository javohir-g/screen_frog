import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')  # Можно заменить модель на flash если нужно

def analyze_text(text: str):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return f"GEMINI SDK error: {e}"
