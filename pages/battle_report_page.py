"""Screen actions for the currently open World of the World battle report."""

import time

from config import settings


class BattleReportPage:
    def __init__(self, driver):
        self.driver = driver

    def screenshot(self) -> bytes:
        return self.driver.get_screenshot_as_png()

    def swipe_report_up(self) -> None:
        self._drag_report('up')

    def drag_report_down(self) -> None:
        """Move toward the beginning of the report before extraction starts."""
        self._drag_report('down')

    def _drag_report(self, direction: str) -> None:
        size = self.driver.get_window_size()
        viewport = settings.REPORT_VIEWPORT
        left = round(size['width'] * viewport['left'])
        top = round(size['height'] * viewport['top'])
        width = round(size['width'] * (viewport['right'] - viewport['left']))
        height = round(size['height'] * (viewport['bottom'] - viewport['top']))

        x = left + round(width * 0.42)
        low_y = top + round(height * 0.88)
        high_y = top + round(height * 0.38)
        start_y, end_y = (low_y, high_y) if direction == 'up' else (high_y, low_y)

        self.driver.execute_script('mobile: dragGesture', {
            'startX': x,
            'startY': start_y,
            'endX': x,
            'endY': end_y,
            'speed': 500,
        })
        time.sleep(0.7)

    def is_bottom_hint_visible(self, lines: list[str]) -> bool:
        hints = ('到底了', '没有更多', '已无更多', '战报结束')
        combined = ''.join(lines)
        return any(hint in combined for hint in hints)
