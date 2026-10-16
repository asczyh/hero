import time

import cv2
import numpy as np
from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class HeroPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def touch_gm(self):
        """点击 GM 按钮图片。"""
        self.touch_img("GM.png")
        self.wait_img("GM界面打开标志.png", timeout=10)

    def gm_input(self, text: str = "恺撒",count:int=0):
        """在 GM 输入框输入文本，并发送一次回车确认。 需要打开GM界面，不需要打开输入栏"""
        self.touch_img("GM输入框.png")
        for i in range(20):
            self.device.keyevent("KEYCODE_DEL")
        self.device.text(text, enter=False, search=True)
        self.gm_execute(count)

    def gm_execute(self,count:int=1):
        """执行第一条GM time次"""
        for i in range(count):
            self.device.touch(rc(420,125))

    def touch_blank(self):
        """Dismiss every visible blank-area prompt; zero occurrences is normal."""
        count = 0
        while True:
            try:
                position = self.wait_img("点击空白处关闭.png", timeout=2)
            except LookupError:
                break
            self.device.touch(position)
            count += 1
            sleep(0.3)
        return count

    def touch_home(self, timeout: float = 5) -> tuple[int, int]:
        """Click the center hex of the seven-hex green home outline."""
        deadline = time.monotonic() + timeout
        stable_centers = []
        kernel = np.ones((3, 3), dtype=np.uint8)
        lower_green = np.array([25, 55, 80], dtype=np.uint8)
        upper_green = np.array([80, 255, 255], dtype=np.uint8)

        while time.monotonic() < deadline:
            screenshot = self._snapshot_upright()
            if screenshot is None or screenshot.ndim != 3 or screenshot.shape[2] < 3:
                raise LookupError("无法读取模拟器截图，未执行主城点击")

            height, width = screenshot.shape[:2]
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask = cv2.morphologyEx(
                mask, cv2.MORPH_CLOSE, kernel, iterations=2
            )
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            candidates = []
            for contour in contours:
                area = cv2.contourArea(contour)
                x, y, box_width, box_height = cv2.boundingRect(contour)
                if (
                    area < width * height * 0.006
                    or box_width < width * 0.08
                    or box_height < height * 0.08
                    or x <= 0
                    or y <= 0
                    or x + box_width >= width
                    or y + box_height >= height
                ):
                    continue

                ratio = box_width / box_height
                if not 1.15 <= ratio <= 1.75:
                    continue

                perimeter = cv2.arcLength(contour, True)
                polygon = cv2.approxPolyDP(contour, perimeter * 0.02, True)
                if not 6 <= len(polygon) <= 12:
                    continue

                center_x = x + box_width / 2
                center_y = y + box_height / 2

                # The background changes; use the green outline's bounds for the center.
                candidates.append((area, (round(center_x), round(center_y))))

            if candidates:
                _, center = max(candidates, key=lambda item: item[0])
                if stable_centers and max(
                    abs(center[0] - previous[0]) + abs(center[1] - previous[1])
                    for previous in stable_centers
                ) > 8:
                    stable_centers.clear()
                stable_centers.append(center)

                if len(stable_centers) >= 3:
                    center_x = round(
                        sorted(point[0] for point in stable_centers[-3:])[1]
                    )
                    center_y = round(
                        sorted(point[1] for point in stable_centers[-3:])[1]
                    )
                    position = (center_x, center_y)
                    self.device.touch(position)
                    return position
            else:
                stable_centers.clear()

            time.sleep(0.2)

        raise LookupError(
            "未能稳定识别完整的绿色七格主城边界，未执行点击；"
        )


