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
        self.touch_img("英雄_信息.png")
        sleep(0.5)

    def button_dismantle(self):
        return  self.touch_img("英雄_分解.png")

    def touch_hero_pos(self,pos=1):
        x=pos*260-95
        self.device.touch(rc(x,400))

    def back_to_hero(self):
        while True:
            if self.exist_img("英雄_界面.png"):
                break
            keyevent("BACK")
            if self.exist_img("确定.png"):
                keyevent("BACK")
            if self.exist_img("地图_主城标志.png"):
                self.touch_img("地图_英雄标志.png")

    def read_skill_exp(self):
        return  self.read_text_in_region(rc(1215,20),rc(1350,50))
    def red_gold_skill_page(self):
        return self.read_text_in_region(rc(1275, 12), rc(1400, 58))
    def red_silver_skill_page(self):
        return self.read_text_in_region(rc(1105, 12), rc(1230, 58))
    def enter_skill_exp(self):
        self.device.touch(rc(1295,35))

    def enter_skill_page(self):
        self.device.touch(rc(1480,35))



