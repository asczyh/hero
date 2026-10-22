"""读取当前打开的 MuMu 战报，并将识别文本保存到 output/。"""

import re
from datetime import datetime
from pathlib import Path

from common.device import connect_mumu
from common.ocr_reader import OcrReader, append_unseen_lines
from config import settings
from pages.battle_report_page import BattleReportPage


def main() -> Path:
    device = connect_mumu()
    try:
        page = BattleReportPage(device)
        reader = OcrReader()
        initial_screenshot = page.screenshot()
        # 顶部多留一些空间以包含回合标题，避免被 OCR 的裁边过滤规则去掉；
        # 当前画面的 REPORT_VIEWPORT 起点离标题太近。
        start_check_viewport = {**settings.REPORT_VIEWPORT, 'top': 0.12}
        start_check_lines = reader.read_lines(initial_screenshot, start_check_viewport)
        if not any(re.search(r'第\s*1\s*回合', line) for line in start_check_lines):
            raise RuntimeError('请先选择左侧“1”，并将战报停在第1回合开头，再运行脚本。')
        opening_lines = [
            line for line in start_check_lines
            if re.search(r'第\s*1\s*回合', line) or line.strip() == '回合开始'
        ]
        # 回合标题和“回合开始”位于 REPORT_OCR_VIEWPORT 上方。先保留这些开头文本，
        # 后续滑动时仍只对战报面板进行 OCR。
        initial_lines = reader.read_lines(initial_screenshot, settings.REPORT_OCR_VIEWPORT)

        saved_lines: list[str] = opening_lines
        no_new_text_count = 0

        for swipe_count in range(settings.REPORT_MAX_SWIPES + 1):
            lines = initial_lines if swipe_count == 0 else reader.read_lines(
                page.screenshot(), settings.REPORT_OCR_VIEWPORT
            )
            added = append_unseen_lines(saved_lines, lines)
            print(f'画面 {swipe_count + 1}: OCR {len(lines)} 行，新增 {added} 行')

            if page.is_bottom_hint_visible(lines):
                print('检测到底部提示，停止读取。')
                break

            if swipe_count == settings.REPORT_MAX_SWIPES:
                print('达到最大滑动次数，停止读取。')
                break

            if added == 0:
                no_new_text_count += 1
                if no_new_text_count >= settings.REPORT_NO_NEW_TEXT_LIMIT:
                    print('连续两次滑动没有新文字，按到底处理。')
                    break
            else:
                no_new_text_count = 0

            page.swipe_report_up()

        output_dir = Path(__file__).resolve().parent / settings.REPORT_OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f'battle_report_{datetime.now():%Y%m%d_%H%M%S}.txt'
        output_file.write_text('\n'.join(saved_lines) + '\n', encoding='utf-8')
        print(f'战报已保存：{output_file}')
        return output_file
    finally:
        device.disconnect()


if __name__ == '__main__':
    main()
