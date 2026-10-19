from pages.base_page import BasePage
from pages.hero_page import HeroPage


class MapPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def enter_center_page(self):
        self.touch_img("地图_主城标志.png")
        self.touch_img("市中心按钮.png")

    def build_barracks(self):
        self.touch_img("建造_军营.png")
        self.touch_img("建造_前往建造.png")
        self.touch_img("确定.png")
        self.touch_blank()