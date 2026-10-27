import time

import cv2
import numpy as np
from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class SkillPage(BasePage):
    def __init__(self, device):
        super().__init__(device)


    def enter_exp_page(self):
        self.device.touch(rc(1370,30))

    import time

    def get_exp(self):
        deadline = time.monotonic() + 5
        self.enter_exp_page()

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise LookupError("2 秒内未找到技能兑换页面")

            try:
                self.wait_img(
                    "技能_兑换.png",
                    timeout=min(0.3, remaining),
                )
                break
            except LookupError:
                if time.monotonic() >= deadline:
                    raise
                self.enter_exp_page()

        exp = int(self.read_text_in_region(rc(265, 840), rc(365, 870)))
        keyevent("BACK")
        self.wait_img("技能_重置.png")
        return exp

    def upgrade_one(self):
        self.touch_img("技能_强化一级.png")
        sleep(1)

    def upgrade_max(self):
        self.touch_img("技能_强化至满级.png")
        sleep(1)

    def reset(self):
        self.touch_img("技能_重置.png")
        self.confirm()

    def get_level(self):
        return self.read_text_in_region(rc(320,485),rc(415,525))    #返回值为str，例如 1级








