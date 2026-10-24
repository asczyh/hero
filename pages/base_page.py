"""用于图像识别和文本交互的 Airtest 通用辅助方法。"""

from __future__ import annotations
from datetime import datetime
import time
from pathlib import Path

import numpy as np
from airtest.core.api import Template
from airtest.core.helper import G
from PIL import Image
from rapidocr import RapidOCR


_IMAGE_TEMPLATE_DIR = str(Path(__file__).resolve().parents[1] / 'assets' / 'img')
if _IMAGE_TEMPLATE_DIR not in G.BASEDIR:
    G.BASEDIR.insert(0, _IMAGE_TEMPLATE_DIR)


class BasePage:
    def __init__(self, device):
        self.device = device
        self._ocr = None
        self.last_match_confidence: float | None = None

    def _snapshot_upright(self) -> np.ndarray:
        """返回与 Airtest 点击坐标对齐的截图。"""
        image = Image.fromarray(self.device.snapshot())
        width, height = self.device.get_current_resolution()
        if image.size == (height, width) and width > height:
            image = image.transpose(Image.Transpose.ROTATE_270)
        return np.asarray(image)

    def save_screenshot(self, filename: str | None = None) -> Path:
        """截取当前模拟器画面并保存到项目的 output 目录。"""
        output_dir = Path(__file__).resolve().parents[1] / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = f"screenshot_{datetime.now():%Y%m%d_%H%M%S_%f}.png"
        elif Path(filename).suffix.lower() != ".png":
            raise ValueError("截图文件名必须以 .png 结尾")

        screenshot_path = output_dir / filename
        Image.fromarray(self._snapshot_upright()).save(screenshot_path)
        return screenshot_path

    def touch_img(
        self,
        image_path: str | Path,
        timeout: float = 10,
        threshold: float = 0.7,
        show_position: bool = False,
    ):
        """查找并点击指定名称或路径的图片模板。"""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"touch_img 的图片参数必须以 .png 结尾，收到：{image_path!s}。"
                "示例：page.touch_img('市中心_新建设施图标.png')"
            )
        position = self.wait_img(image_path, timeout, threshold)
        if show_position:
            print(f"点击图片 {image_path}，坐标：{position}")
        return self.device.touch(position)

    def exist_img(
        self,
        image_path: str | Path,
        timeout: float = 1,
        threshold: float = 0.7,
    ) -> bool:
        """等待图片出现并保存最高匹配度，不执行点击。"""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"exist_img 的图片参数必须以 .png 结尾，收到：{image_path!s}"
            )

        template = Template(str(image_path), threshold=0)
        deadline = time.monotonic() + timeout
        self.last_match_confidence = 0.0
        while True:
            matches = template.match_all_in(self._snapshot_upright()) or []
            self.last_match_confidence = max(
                (match["confidence"] for match in matches),
                default=0.0,
            )
            if self.last_match_confidence >= threshold:
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.25)

    def find_all(self, image_path: str | Path) -> list[tuple[int, int]]:
        """返回屏幕上所有匹配图片的中心坐标。"""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"find_all 的图片参数必须以 .png 结尾，收到：{image_path!s}"
            )
        template = Template(str(image_path))
        matches = template.match_all_in(self._snapshot_upright()) or []
        return [match["result"] for match in matches]

    def touch_img_if_present(
        self, image_path: str | Path, timeout: float = 1
    ) -> bool:
        """若图片在超时前出现则点击，否则继续执行。"""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"touch_img_if_present 的图片参数必须以 .png 结尾，收到：{image_path!s}"
            )
        try:
            position = self.wait_img(image_path, timeout)
        except LookupError:
            print(f"未找到图片：{image_path}（等待 {timeout} 秒）")
            return False
        self.device.touch(position)
        return True

    def touch_img_in_region(
        self,
        image_path: str | Path,
        top_left: tuple[float, float],
        bottom_right: tuple[float, float],
        timeout: float = 5,
    ):
        """在相对坐标定义的矩形区域内查找并点击图片。"""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"touch_img_in_region 的图片参数必须以 .png 结尾，收到：{image_path!s}"
            )
        if len(top_left) != 2 or len(bottom_right) != 2:
            raise ValueError("top_left 和 bottom_right 都必须是 (x, y) 坐标")

        left_ratio, top_ratio = top_left
        right_ratio, bottom_ratio = bottom_right
        if not all(0 <= value <= 1 for value in (*top_left, *bottom_right)):
            raise ValueError("相对坐标必须在 0 到 1 之间")
        if right_ratio <= left_ratio or bottom_ratio <= top_ratio:
            raise ValueError(f"无效的匹配区域：{top_left!r}, {bottom_right!r}")

        template = Template(str(image_path))
        deadline = time.monotonic() + min(timeout, 5)
        while True:
            screenshot = self._snapshot_upright()
            height, width = screenshot.shape[:2]
            left = round(left_ratio * width)
            top = round(top_ratio * height)
            right = round(right_ratio * width)
            bottom = round(bottom_ratio * height)
            if right <= left or bottom <= top:
                raise ValueError("相对坐标换算后的匹配区域为空")

            cropped = screenshot[top:bottom, left:right]
            position = template.match_in(cropped)
            if position is not None:
                position = (position[0] + left, position[1] + top)
                return self.device.touch(position)

            if time.monotonic() >= deadline:
                raise LookupError(
                    f"在区域 {top_left!r} 到 {bottom_right!r} 内未找到图片模板：{image_path}"
                )
            time.sleep(0.25)


    def read_text_in_region(
        self,
        top_left: tuple[float, float],
        bottom_right: tuple[float, float],
        timeout: float = 5,
    ) -> str:
        """识别指定相对区域内的文字并返回，移除数字千位分隔逗号。"""
        if len(top_left) != 2 or len(bottom_right) != 2:
            raise ValueError("top_left 和 bottom_right 都必须是 (x, y) 坐标")
        if not all(0 <= value <= 1 for value in (*top_left, *bottom_right)):
            raise ValueError("相对坐标必须在 0 到 1 之间")
        if bottom_right[0] <= top_left[0] or bottom_right[1] <= top_left[1]:
            raise ValueError(f"无效的识别区域：{top_left!r}, {bottom_right!r}")

        deadline = time.monotonic() + min(timeout, 5)
        while True:
            screenshot = self._snapshot_upright()
            height, width = screenshot.shape[:2]
            left = round(top_left[0] * width)
            top = round(top_left[1] * height)
            right = round(bottom_right[0] * width)
            bottom = round(bottom_right[1] * height)
            if right <= left or bottom <= top:
                raise ValueError("相对坐标换算后的识别区域为空")

            cropped = screenshot[top:bottom, left:right]
            if self._ocr is None:
                self._ocr = RapidOCR()
            result = self._ocr(cropped)
            if result and result.txts:
                text = "".join(str(item) for item in result.txts)
                text = "".join(text.split()).replace(",", "").replace("，", "")
                if text:
                    return text

            if time.monotonic() >= deadline:
                raise LookupError(
                    f"在区域 {top_left!r} 到 {bottom_right!r} 内未识别到文字"
                )
            time.sleep(0.25)

    def touch_img_in_row(
        self,
        image_path: str | Path,
        row_image_path: str | Path,
        timeout: float = 5,
        y_tolerance: int = 25,
    ) -> tuple[int, int]:
        """点击与另一张模板图片处于同一行的匹配项。"""
        for path in (image_path, row_image_path):
            if Path(path).suffix.lower() != ".png":
                raise ValueError(f"图片参数必须以 .png 结尾，收到：{path!s}")

        button_template = Template(str(image_path))
        row_template = Template(str(row_image_path), threshold=0.95)
        deadline = time.monotonic() + min(timeout, 5)
        while True:
            screenshot = self._snapshot_upright()
            row_position = row_template.match_in(screenshot)
            if row_position is not None:
                matches = button_template.match_all_in(screenshot) or []
                if matches:
                    match = min(
                        matches,
                        key=lambda item: abs(item["result"][1] - row_position[1]),
                    )
                    if abs(match["result"][1] - row_position[1]) <= y_tolerance:
                        return self.device.touch(match["result"])

            if time.monotonic() >= deadline:
                raise LookupError(
                    f'未找到图片“{row_image_path}”所在行的按钮：{image_path}'
                )
            time.sleep(0.25)

    def wait_img(
        self, image_path: str | Path, timeout: float = 5, threshold: float = 0.7
    ) -> tuple[int, int]:
        """等待图片模板出现，并返回其中心坐标。"""
        template = Template(str(image_path), threshold=threshold)
        deadline = time.monotonic() + timeout
        while True:
            position = template.match_in(self._snapshot_upright())
            if position is not None:
                return position
            if time.monotonic() >= deadline:
                raise LookupError(f'等待图片模板超时，屏幕上未找到：{image_path}')
            time.sleep(0.25)

    def _find_text_in_image(
        self, screenshot: np.ndarray, target: str
    ) -> tuple[int, int] | None:
        if self._ocr is None:
            self._ocr = RapidOCR()
        result = self._ocr(screenshot)
        if result and result.boxes is not None and result.txts:
            for box, text in zip(result.boxes, result.txts):
                if target.casefold() in str(text).casefold():
                    center_x = round(sum(float(point[0]) for point in box) / len(box))
                    center_y = round(sum(float(point[1]) for point in box) / len(box))
                    return center_x, center_y
        return None

    def _find_text_position(self, target: str, timeout: float) -> tuple[int, int] | None:
        deadline = time.monotonic() + timeout
        while True:
            position = self._find_text_in_image(self._snapshot_upright(), target)
            if position is not None:
                return position
            if time.monotonic() >= deadline:
                return None
            time.sleep(0.25)



    def touch_blank(self):
        """关闭所有可见的“点击空白处”提示；提示出现零次也是正常情况。"""
        count = 0
        while True:
            try:
                position = self.wait_img("点击空白处关闭.png", timeout=2)
            except LookupError:
                break
            self.device.touch(position)
            count += 1
            time.sleep(0.3)
        return count
