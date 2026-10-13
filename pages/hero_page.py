from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class HeroPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def touch_gm(self):
        """点击 GM 按钮图片。"""
        self.touch_img("GM.png")
        self.wait_img("GM界面打开标志.png", timeout=10)

    def gm_input(self, text: str = "恺撒",count:int=0):
        """在 GM 输入框输入文本，并发送一次回车确认。 需要打开GM界面，不需要打开输入栏"""
        self.touch_img("GM输入框.png")
        for i in range(20):
            self.device.keyevent("KEYCODE_DEL")
        self.device.text(text, enter=False, search=True)
        self.gm_execute(count)

    def gm_execute(self,count:int=1):
        """执行第一条GM time次"""
        for i in range(count):
            self.device.touch(rc(340,100))


