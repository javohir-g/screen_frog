try:
    import dxcam
    import cv2
except Exception:
    dxcam = None
    cv2 = None


class DirectXCapture:
    def __init__(self):
        self.camera = None
        self.setup_directx()

    def setup_directx(self):
        """Настройка DirectX захвата"""
        if dxcam is None:
            return
        try:
            self.camera = dxcam.create(output_idx=0, output_color="BGR")
            if self.camera is not None:
                self.camera.start(target_fps=60, video_mode=False)
        except Exception:
            self.camera = None

    def capture_region(self, region=None):
        """Захват региона (x1, y1, x2, y2). Возвращает BGR numpy или None"""
        if self.camera is None:
            return None
        try:
            frame = self.camera.get_latest_frame()
            if frame is not None and region is not None:
                x1, y1, x2, y2 = region
                frame = frame[y1:y2, x1:x2]
            return frame
        except Exception:
            return None


