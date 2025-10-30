import os
import google.generativeai as genai
from prompt_manager import load_prompt

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')  # Можно заменить модель на flash если нужно

def analyze_text(text: str):
    system_prompt = load_prompt()
    prompt = f"{system_prompt}\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"GEMINI SDK error: {e}"