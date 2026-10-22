"""当前已打开战报页面的界面操作。"""

from io import BytesIO
import time

from config import settings
from PIL import Image


class BattleReportPage:
    def __init__(self, device):
        self.device = device

    def screenshot(self) -> bytes:
        screenshot = Image.fromarray(self.device.snapshot())
        # MuMu 截图相对触摸坐标旋转了 90 度：Airtest 原始画面为 900×1600，
        # 但触摸坐标空间为 1600×900。应用战报/OCR 区域前，先将截图转到触摸分辨率。
        width, height = self.device.get_current_resolution()
        if screenshot.size == (height, width) and width > height:
            screenshot = screenshot.transpose(Image.Transpose.ROTATE_270)
        buffer = BytesIO()
        screenshot.save(buffer, format='PNG')
        return buffer.getvalue()

    def swipe_report_up(self) -> None:
        self._drag_report('up')

    def drag_report_down(self) -> None:
        """开始提取前，先滑到战报开头。"""
        self._drag_report('down')

    def _drag_report(self, direction: str) -> None:
        #计算战报区域，计算滑动起点和终点
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
