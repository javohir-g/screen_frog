from PIL import ImageGrab
import io

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
    # Fallback to full screen grab
    img = ImageGrab.grab()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
