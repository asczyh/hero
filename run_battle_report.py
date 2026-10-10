"""Read the open MuMu battle report and save its text to output/."""

import re
from datetime import datetime
from pathlib import Path

from common.device import get_existing_mumu_driver
from common.ocr_reader import OcrReader, append_unseen_lines
from config import settings
from pages.battle_report_page import BattleReportPage


def main() -> Path:
    driver = get_existing_mumu_driver()
    try:
        current_package = driver.current_package
        if current_package and current_package != settings.GAME_PACKAGE:
            raise RuntimeError(
                f'当前前台应用是 {current_package}，请先在 MuMu 中打开《世界启元》的战报页。'
            )

        page = BattleReportPage(driver)
        reader = OcrReader()
        initial_lines = reader.read_lines(page.screenshot(), settings.REPORT_OCR_VIEWPORT)
        if not any(re.search(r'第\s*1\s*回合', line) for line in initial_lines):
            raise RuntimeError('请先选择左侧“1”，并将战报停在第1回合开头，再运行脚本。')

        saved_lines: list[str] = []
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
        driver.quit()


if __name__ == '__main__':
    main()
