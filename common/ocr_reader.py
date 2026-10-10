"""OCR and overlap-aware text assembly for screenshots of battle reports."""

from __future__ import annotations

import io
import re
from difflib import SequenceMatcher
from typing import Iterable

from PIL import Image
from rapidocr import RapidOCR


class OcrReader:
    def __init__(self):
        self.engine = RapidOCR()

    def read_lines(self, screenshot_png: bytes, viewport: dict[str, float]) -> list[str]:
        """OCR only the report body and return detected lines in reading order."""
        image = Image.open(io.BytesIO(screenshot_png)).convert('RGB')
        width, height = image.size
        left = round(width * viewport['left'])
        top = round(height * viewport['top'])
        right = round(width * viewport['right'])
        bottom = round(height * viewport['bottom'])
        crop = image.crop((left, top, right, bottom))

        result = self.engine(crop)
        if not result or not result.txts or result.boxes is None:
            return []

        lines = []
        for box, text in zip(result.boxes, result.txts):
            clean = re.sub(r'\s+', ' ', str(text)).strip()
            if not clean or clean in {'简略战报', '收起战报', 'uv1-'}:
                continue
            # Each box is four (x, y) points, relative to the cropped image.
            y = sum(float(point[1]) for point in box) / len(box)
            x = min(float(point[0]) for point in box)
            lines.append((y, x, clean))

        lines.sort(key=lambda item: (item[0], item[1]))
        return [line for _, _, line in lines]


def _normalized(line: str) -> str:
    return re.sub(r'[\s，。！？；：、,.!?;:（）()\[\]【】]', '', line).lower()


def _same_line(left: str, right: str) -> bool:
    a, b = _normalized(left), _normalized(right)
    if not a or not b:
        return False
    if a == b:
        return True
    # OCR sometimes changes a single character at a frame boundary.
    return min(len(a), len(b)) >= 5 and SequenceMatcher(None, a, b).ratio() >= 0.82


def append_unseen_lines(saved: list[str], current: Iterable[str]) -> int:
    """Append a frame after removing its longest suffix/prefix overlap."""
    incoming = list(current)
    overlap = 0
    max_overlap = min(len(saved), len(incoming), 30)
    for size in range(1, max_overlap + 1):
        if all(_same_line(a, b) for a, b in zip(saved[-size:], incoming[:size])):
            overlap = size

    new_lines = incoming[overlap:]
    saved.extend(new_lines)
    return len(new_lines)
