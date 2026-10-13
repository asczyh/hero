"""Screen actions for the currently open World of the World battle report."""

from io import BytesIO
import time

from config import settings
from PIL import Image


class BattleReportPage:
    def __init__(self, device):
        self.device = device

    def screenshot(self) -> bytes:
        screenshot = Image.fromarray(self.device.snapshot())
        # MuMu reports a 90-degree physical rotation: Airtest's raw frame is
        # 900x1600 even though its touch coordinate space is 1600x900. Normalize
        # captures to the touch resolution before applying report/OCR viewports.
        width, height = self.device.get_current_resolution()
        if screenshot.size == (height, width) and width > height:
            screenshot = screenshot.transpose(Image.Transpose.ROTATE_270)
        buffer = BytesIO()
        screenshot.save(buffer, format='PNG')
        return buffer.getvalue()

    def swipe_report_up(self) -> None:
        self._drag_report('up')

    def drag_report_down(self) -> None:
        """Move toward the beginning of the report before extraction starts."""
        self._drag_report('down')

    def _drag_report(self, direction: str) -> None:
        width, height = self.device.get_current_resolution()
        viewport = settings.REPORT_VIEWPORT
        left = round(width * viewport['left'])
        top = round(height * viewport['top'])
        viewport_width = round(width * (viewport['right'] - viewport['left']))
        viewport_height = round(height * (viewport['bottom'] - viewport['top']))

        x = left + round(viewport_width * 0.42)
        start_y = top + round(viewport_height * 0.88)
        end_y = start_y - round(viewport_height * settings.REPORT_SCROLL_PERCENT)
        if direction == 'down':
            start_y, end_y = end_y, start_y

        self.device.swipe((x, start_y), (x, end_y), duration=0.5)
        time.sleep(0.7)

    def is_bottom_hint_visible(self, lines: list[str]) -> bool:
        hints = ('到底了', '没有更多', '已无更多', '战报结束')
        combined = ''.join(lines)
        return any(hint in combined for hint in hints)
