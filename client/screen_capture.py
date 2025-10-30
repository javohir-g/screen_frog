import time
import io
from typing import Optional, Tuple

import psutil
from PIL import Image
import mss

try:
    import win32gui
    import win32process
except Exception:
    win32gui = None
    win32process = None


class SEBCapture:
    def __init__(self):
        self.seb_hwnd = None

    def find_seb_window(self):
        """Поиск окна SEB с улучшенной логикой"""
        if win32gui is None:
            return []
        windows = []

        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                process_name = self.get_process_name(hwnd)
                if (("SEB" in window_text.upper() or "Safe Exam Browser" in window_text or
                     (process_name and "seb" in process_name.lower())) and
                        win32gui.IsWindowVisible(hwnd)):
                    windows.append({
                        'hwnd': hwnd,
                        'text': window_text,
                        'process': process_name
                    })
            return True

        win32gui.EnumWindows(enum_windows_proc, None)
        return windows

    def get_process_name(self, hwnd):
        """Получение имени процесса по handle окна"""
        if win32process is None:
            return "Unknown"
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception:
            return "Unknown"

    def capture_seb_directx(self) -> Optional[Image.Image]:
        """Попытка захвата через DirectX (dxcam)"""
        try:
            import dxcam
            import cv2
            camera = dxcam.create()
            frame = camera.grab()
            if frame is None:
                return None
            # dxcam returns BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame)
        except Exception:
            return None

    def capture_using_desktop_duplication(self) -> Optional[Image.Image]:
        """Использование Desktop Duplication API через dxcam с регионом окна SEB"""
        try:
            import dxcam
            import cv2
            cam = dxcam.create(output_idx=0, output_color="BGR")

            if not self.seb_hwnd:
                windows = self.find_seb_window()
                if windows:
                    self.seb_hwnd = windows[0]['hwnd']

            if self.seb_hwnd and win32gui is not None:
                left, top, right, bottom = win32gui.GetWindowRect(self.seb_hwnd)
                region = (left, top, right, bottom)
                bgr = cam.grab(region=region)
                if bgr is None:
                    return None
                rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                return Image.fromarray(rgb)
        except Exception:
            return None
        return None

    def bypass_window_protection(self, hwnd) -> bool:
        """Попытка обхода защиты окна"""
        try:
            if win32gui is None:
                return False
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000

            current_style = win32gui.GetWindowLong(hwnd, GWL_EXSTYLE)
            new_style = current_style & ~WS_EX_LAYERED
            win32gui.SetWindowLong(hwnd, GWL_EXSTYLE, new_style)

            return True
        except Exception:
            return False

    def _grab_bbox(self, bbox: Tuple[int, int, int, int]) -> Optional[Image.Image]:
        """Захват области экрана через mss (без COM). bbox=(left, top, right, bottom)"""
        try:
            left, top, right, bottom = bbox
            width = max(0, right - left)
            height = max(0, bottom - top)
            if width == 0 or height == 0:
                return None
            with mss.mss() as sct:
                shot = sct.grab({"left": left, "top": top, "width": width, "height": height})
                # shot is BGRA
                img = Image.frombytes("RGB", (shot.width, shot.height), shot.rgb)
                return img
        except Exception:
            return None

    def try_alternative_methods(self) -> Optional[Image.Image]:
        """Альтернативные методы захвата"""
        try:
            windows = self.find_seb_window()
            if windows and win32gui is not None:
                hwnd = windows[0]['hwnd']
                self.bypass_window_protection(hwnd)
                # Захват через mss по прямоугольнику окна
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                return self._grab_bbox((left, top, right, bottom))
        except Exception:
            return None
        return None

    def capture_best_effort(self) -> Image.Image:
        """Мульти-подход: DirectX → Desktop Duplication → альтернативы → полный экран"""
        methods = [
            self.capture_seb_directx,
            self.capture_using_desktop_duplication,
            self.try_alternative_methods,
        ]
        for method in methods:
            img = method()
            if img is not None:
                return img
        # Fallback: полный экран через mss
        try:
            with mss.mss() as sct:
                mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                shot = sct.grab(mon)
                return Image.frombytes("RGB", (shot.width, shot.height), shot.rgb)
        except Exception:
            # Последний шанс: пустая картинка 1x1, чтобы не падать
            return Image.new("RGB", (1, 1), color=(0, 0, 0))

    def capture_bytes_png(self) -> bytes:
        image = self.capture_best_effort()
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        return buf.getvalue()


