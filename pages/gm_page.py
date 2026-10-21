import time

import cv2
import numpy as np
from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class GmPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def open(self):
        """点击 GM 按钮图片。"""
        self.touch_img("GM.png")
        self.wait_img("GM界面打开标志.png", timeout=10)


    def input(self, text: str = "恺撒", count: int = 0):
        """在 GM 输入框输入文本，并发送一次回车确认。 需要打开GM界面，不需要打开输入栏"""
        self.touch_img("GM输入框.png")
        for i in range(20):
            self.device.keyevent("KEYCODE_DEL")
        self.device.text(text, enter=False, search=True)
        self.execute(count)

    def execute(self, count: int = 1):
        """执行第一条GM time次"""
        for i in range(count):
            self.device.touch(rc(420, 125))

    def exit(self):
        self.touch_img("退出GM.png")





