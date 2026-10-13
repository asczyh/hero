from pages.base_page import BasePage


class HeroPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def click_gm(self):
        """点击 GM 按钮图片。"""
        return self.click_img("GM.png")
