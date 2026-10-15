"""Reusable Airtest helpers for image- and text-based screen interaction."""

from __future__ import annotations

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

    def _snapshot_upright(self) -> np.ndarray:
        """Return a screenshot aligned with Airtest's touch coordinates."""
        image = Image.fromarray(self.device.snapshot())
        width, height = self.device.get_current_resolution()
        if image.size == (height, width) and width > height:
            image = image.transpose(Image.Transpose.ROTATE_270)
        return np.asarray(image)

    def touch_img(self, image_path: str | Path, timeout: float = 5):
        """Find and click an image template by its name or path."""
        if Path(image_path).suffix.lower() != ".png":
            raise ValueError(
                f"touch_img 的图片参数必须以 .png 结尾，收到：{image_path!s}。"
                "示例：page.touch_img('市中心_新建设施图标.png')"
            )
        position = self.wait_img(image_path, timeout)
        return self.device.touch(position)

    def touch_img_in_row(
        self,
        image_path: str | Path,
        row_image_path: str | Path,
        timeout: float = 5,
        y_tolerance: int = 25,
    ) -> tuple[int, int]:
        """Click an image match on the same row as another image template."""
        for path in (image_path, row_image_path):
            if Path(path).suffix.lower() != ".png":
                raise ValueError(f"图片参数必须以 .png 结尾，收到：{path!s}")

        button_template = Template(str(image_path))
        row_template = Template(str(row_image_path), threshold=0.95)
        deadline = time.monotonic() + timeout
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

    def touch_extreme_img(
        self,
        image_path: str | Path,
        direction: str = "top",
        timeout: float = 5,
    ) -> tuple[int, int]:
        """Wait for matching images, then click the one nearest the requested screen edge."""
        direction_axes = {
            "top": (1, False),
            "bottom": (1, True),
            "left": (0, False),
            "right": (0, True),
        }
        if direction not in direction_axes:
            raise ValueError(
                f"direction must be one of {', '.join(direction_axes)}, got: {direction!r}"
            )

        template = Template(str(image_path))
        deadline = time.monotonic() + timeout
        while True:
            matches = template.match_all_in(self._snapshot_upright())
            if matches:
                axis, choose_largest = direction_axes[direction]
                match = (max if choose_largest else min)(
                    matches,
                    key=lambda item: item["result"][axis],
                )
                return self.device.touch(match["result"])

            if time.monotonic() >= deadline:
                raise LookupError(f'等待图片模板超时，屏幕上未找到：{image_path}')
            time.sleep(0.25)


    def wait_img(self, image_path: str | Path, timeout: float = 5) -> tuple[int, int]:
        """Wait for an image template to appear and return its center position."""
        template = Template(str(image_path))
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

    def click_text(self, text: str, timeout: float = 5) -> bool:
        """OCR visible text and tap its center with the connected Airtest device."""
        position = self._find_text_position(text, timeout)
        if position is None:
            raise LookupError(f'屏幕上未找到文字：{text}')
        self.device.touch(position)
        return True

    def touch_text_if_present(self, text: str, timeout: float = 1) -> bool:
        """Tap visible text if it appears before timeout; otherwise do nothing."""
        position = self._find_text_position(text, timeout)
        if position is None:
            return False
        self.device.touch(position)
        return True
