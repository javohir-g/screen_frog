from PIL import ImageGrab
import io

def take_screenshot():
    img = ImageGrab.grab()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
