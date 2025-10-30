def load_prompt():
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(user_text: str):
    prompt = load_prompt()
    return f"{prompt}\n\n---\n{user_text}"
