import os
import time
import random
import requests


def main():
    # Config
    url = os.environ.get("KEEPALIVE_URL") or "https://screen-frog.onrender.com/docs"
    base_interval_min = int(os.environ.get("KEEPALIVE_INTERVAL_MIN", "12"))
    jitter_min = int(os.environ.get("KEEPALIVE_JITTER_MIN", "3"))
    timeout_s = int(os.environ.get("KEEPALIVE_TIMEOUT_S", "10"))

    print(f"KeepAlive started. URL={url}, interval≈{base_interval_min}±{jitter_min} min")

    while True:
        try:
            t0 = time.strftime("%Y-%m-%d %H:%M:%S")
            r = requests.get(url, timeout=timeout_s)
            print(f"[{t0}] {r.status_code} {len(r.content)} bytes from {url}")
        except Exception as e:
            print(f"[WARN] KeepAlive request failed: {e}")

        # Sleep with jitter to look less bot-like
        sleep_min = base_interval_min + random.randint(-jitter_min, jitter_min)
        sleep_min = max(1, sleep_min)
        time.sleep(sleep_min * 60)


if __name__ == "__main__":
    main()


