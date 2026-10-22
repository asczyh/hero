"""识别战报截图中的文字，并通过重叠内容拼接文本。"""

from __future__ import annotations

import io
import re
import statistics
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import Iterable

from PIL import Image
from rapidocr import RapidOCR


@dataclass(frozen=True)
class TextBox:
    text: str
    left: float
    top: float
    right: float
    bottom: float

    @property
    def center_x(self) -> float:
        return (self.left + self.right) / 2

    @property
    def center_y(self) -> float:
        return (self.top + self.bottom) / 2

    @property
    def height(self) -> float:
        return self.bottom - self.top


class OcrReader:
    def __init__(self):
        self.engine = RapidOCR()

    def read_lines(self, screenshot_png: bytes, viewport: dict[str, float]) -> list[str]:
        """仅识别战报正文，并按阅读顺序返回检测到的文本行。"""
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

        boxes: list[TextBox] = []
        for box, text in zip(result.boxes, result.txts):
            clean = re.sub(r'\s+', ' ', str(text)).strip()
            if not clean or clean in {'简略战报', '收起战报', 'uv1-'}:
                continue
            # 每个文本框由相对于裁剪图像的四个 (x, y) 点组成。
            xs = [float(point[0]) for point in box]
            ys = [float(point[1]) for point in box]
            # 游戏会裁掉滚动面板边缘处只显示一部分的文本行。
            # 忽略这些片段，下一帧的重叠区域会包含完整文本行。
            if min(ys) < 20 or max(ys) > crop.height - 8:
                continue
            boxes.append(TextBox(clean, min(xs), min(ys), max(xs), max(ys)))

        return _layout_text_boxes(boxes, crop.width)


_METRIC_PATTERNS = {
    '兵力': re.compile(r'兵力\s*[:：]?\s*([0-9,]+)'),
    '杀敌': re.compile(r'杀敌\s*[:：]?\s*([0-9,]+)'),
    '恢复': re.compile(r'恢复\s*[:：]?\s*([0-9,]+)'),
}


def _layout_text_boxes(boxes: list[TextBox], image_width: int) -> list[str]:
    """按基线对 OCR 文本框分组，再根据位置关系合并行动行和数值字段。"""
    if not boxes:
        return []

    boxes.sort(key=lambda item: (item.center_y, item.left))
    box_indices = {id(box): index for index, box in enumerate(boxes)}
    typical_height = statistics.median(max(1.0, box.height) for box in boxes)
    row_tolerance = max(10.0, typical_height * 0.60)
    rows: list[list[TextBox]] = []
    for box in boxes:
        if rows:
            row_y = statistics.mean(item.center_y for item in rows[-1])
            if abs(box.center_y - row_y) <= row_tolerance:
                rows[-1].append(box)
                continue
        rows.append([box])

    rows = [row for row in rows if not _is_non_report_row(row)]

    action_rows: list[tuple[int, float, str]] = []
    for row_index, row in enumerate(rows):
        row_text = ' '.join(box.text for box in sorted(row, key=lambda item: item.left))
        match = re.search(r'(.{0,24}开始行动)', row_text)
        if match:
            action_rows.append((row_index, statistics.mean(box.center_y for box in row), match.group(1).strip()))

    consumed: set[int] = set()
    output: list[tuple[float, str]] = []
    # 数值标签的检测框垂直位置可能与行动文本略有偏差。
    # 由于只匹配右侧列中带标签的字段，因此可以适当放宽匹配范围。
    metric_tolerance = max(28.0, typical_height * 1.30)

    for action_index, action_y, action_text in action_rows:
        action_row = rows[action_index]
        action_x = min(box.left for box in action_row if '开始行动' in box.text) if any(
            '开始行动' in box.text for box in action_row
        ) else min(box.left for box in action_row)

        nearby_metrics: list[tuple[int, TextBox]] = []
        for row_index, row in enumerate(rows):
            row_y = statistics.mean(box.center_y for box in row)
            if abs(row_y - action_y) > metric_tolerance:
                continue
            for box_index, box in enumerate(boxes):
                is_action_box = '开始行动' in box.text
                is_right_column = box.left > action_x and box.center_x >= image_width * 0.58
                if box in row and (is_right_column or is_action_box):
                    if any(pattern.search(box.text) for pattern in _METRIC_PATTERNS.values()):
                        nearby_metrics.append((box_index, box))

        values: dict[str, str] = {}
        for box_index, box in nearby_metrics:
            for name, pattern in _METRIC_PATTERNS.items():
                match = pattern.search(box.text)
                if match:
                    values[name] = match.group(1).replace(',', '')
                    consumed.add(box_index)

        metric_text = '  '.join(f'{name}:{values[name]}' for name in ('兵力', '杀敌', '恢复') if name in values)
        output.append((action_y, f'{action_text}   {metric_text}'.rstrip()))

    for row_index, row in enumerate(rows):
        if any(index == row_index for index, _, _ in action_rows):
            continue
        text_parts = []
        for box in sorted(row, key=lambda item: item.left):
            box_index = box_indices[id(box)]
            if box_index in consumed:
                continue
            text_parts.append(box.text)
        if text_parts:
            output.append((statistics.mean(box.center_y for box in row), ' '.join(text_parts)))

    output.sort(key=lambda item: item[0])
    return [line for _, line in output]


def _normalized(line: str) -> str:
    return re.sub(r'[\s，。！？；：、,.!?;:（）()\[\]【】]', '', line).lower()


def _is_non_report_row(row: list[TextBox]) -> bool:
    text = ' '.join(box.text for box in sorted(row, key=lambda item: item.left)).strip()
    ui_markers = ('播放倍速', '简略战报', '收起战报', '展开战报')
    if any(marker in text for marker in ui_markers):
        return True
    # 没有标签的数字通常是界面状态栏的残片，而不是战报内容。
    return bool(re.fullmatch(r'[0-9\s,，.。:：/\\+%()（）-]+', text))


def _same_line(left: str, right: str) -> bool:
    a, b = _normalized(left), _normalized(right)
    if not a or not b:
        return False
    if a == b:
        return True
    # OCR 有时会在相邻画面的边界处把一个字符识别成不同内容。
    return min(len(a), len(b)) >= 5 and SequenceMatcher(None, a, b).ratio() >= 0.82


def append_unseen_lines(saved: list[str], current: Iterable[str]) -> int:
    """去除新画面与已有文本之间最长的后缀/前缀重叠后，再追加该画面的文本。"""
    incoming = list(current)
    overlap = 0
    max_overlap = min(len(saved), len(incoming), 30)
    for size in range(1, max_overlap + 1):
        if all(_same_line(a, b) for a, b in zip(saved[-size:], incoming[:size])):
            overlap = size

    new_lines = incoming[overlap:]
    saved.extend(new_lines)
    return len(new_lines)
