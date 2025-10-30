import argparse
import json
import os
import sys
from typing import Optional

import requests


def load_key(explicit_key: Optional[str]) -> Optional[str]:
    if explicit_key:
        return explicit_key.strip()
    # 1) ENV
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key.strip()
    # 2) server/config.json
    cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if cfg.get("openai_key"):
                return cfg["openai_key"].strip()
        except Exception:
            pass
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Check OpenAI API key by making a minimal chat request")
    parser.add_argument("--key", help="OpenAI API key (overrides env/config)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to use (default: gpt-4o-mini)")
    args = parser.parse_args()

    api_key = load_key(args.key)
    if not api_key:
        print("ERROR: No OpenAI API key found. Provide --key, set OPENAI_API_KEY, put key into server/config.json or openai_key.txt")
        return 1

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": "Say 'pong'"}],
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
    except Exception as e:
        print(f"ERROR: Request failed: {e}")
        return 1

    try:
        data = res.json()
    except Exception:
        print(f"ERROR: Non-JSON response (HTTP {res.status_code}): {res.text[:300]}")
        return 1

    if res.status_code != 200:
        msg = (data.get("error") or {}).get("message") if isinstance(data, dict) else None
        print(f"ERROR: HTTP {res.status_code}: {msg or data}")
        return 1

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        print(f"ERROR: Unexpected response: {data}")
        return 1

    print(f"OK: {content}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


