from pages.base_page import BasePage


class HeroPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def click_gm(self):
        """点击 GM 按钮图片。"""
        self.click_img("GM.png")
        self.wait_img("GM界面打开标志.png", timeout=10)
