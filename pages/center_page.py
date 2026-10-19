from pages.base_page import BasePage
from pages.hero_page import HeroPage


class CenterPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def build(self):
        self.touch_img("市中心_新建设施图标.png")

    def build_facility(self):
        self.touch_img_if_present("建造文字按钮.png")
        self.touch_img_if_present("市中心_升级设施.png")
        self.touch_img("加速建造按钮.png")


