import time

import cv2
import numpy as np
from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class HeroPage(BasePage):
    def __init__(self, device):
        super().__init__(device)

    def choose_hero(self, name,count=1):
        matches = self.find_all(name)
        for position in matches[:count]:
            self.device.touch(position)
            sleep(0.1)

    def button_star(self, timeout: float = 5):
        #升星按钮被gm覆盖，因此需要向下便宜点击坐标
        position = self.wait_img("英雄_升星.png", timeout)
        while True:
            self.device.touch((position[0], position[1] - 37))
            if self.exist_img("英雄_升星按钮.png"):
                break

        sleep(0.5)

    def button_info(self):
        return  self.touch_img("英雄_信息.png")

    def button_dismantle(self):
        return  self.touch_img("英雄_分解.png")

    def touch_hero_pos(self,pos=1):
        x=pos*260-95
        self.device.touch(rc(x,400))





