import io
from PIL import Image
import mss

try:
    from .screen_capture import SEBCapture  # when used as package
except Exception:
    try:
        from screen_capture import SEBCapture  # when run as scripts
    except Exception:
        SEBCapture = None

def take_screenshot():
    # Try SEB-aware capture first
    if SEBCapture is not None:
        try:
            seb = SEBCapture()
            data = seb.capture_bytes_png()
            return io.BytesIO(data)
        except Exception:
            pass
    # Fallback to full screen via mss (no COM)
    try:
        with mss.mss() as sct:
            mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            shot = sct.grab(mon)
            img = Image.frombytes("RGB", (shot.width, shot.height), shot.rgb)
    except Exception:
        img = Image.new("RGB", (1, 1), color=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
