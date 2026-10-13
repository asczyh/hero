from pages.base_page import BasePage


class MainPage(BasePage):
    def handle_privacy_policy(self):
        """Tap the consent button when a privacy prompt is visible."""
        if not self.click_text_if_present('同意并继续', timeout=1):
            self.click_text_if_present('同意', timeout=1)

    def click_skip_ad(self):
        """Skip an advertisement when its button is visible."""
        self.click_text_if_present('跳过', timeout=1)

    def click_search_box(self):
        """Tap the visible search control using OCR."""
        self.click_text('搜索')

    def input_search_text(self, text):
        """Type a query into the focused search box and submit it."""
        self.device.text(text, enter=False)
        self.device.keyevent('ENTER')
