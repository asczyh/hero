import time

import cv2
import numpy as np
from pages.base_page import BasePage
from airtest.core.api import *
from utils import *
class ExpPage(BasePage):
    def __init__(self, device):
        super().__init__(device)


    def read_skill_exp(self):
        return  int(self.read_text_in_region(rc(265,840),rc(365,870)))

    def read_skill_paper(self):
        return  int(self.read_text_in_region(rc(265,840),rc(365,870)))

    def read_gold(self):
        return int(self.read_text_in_region(rc(1275, 12), rc(1400, 58)))

    def read_silver(self):
        return int(self.read_text_in_region(rc(1105, 12), rc(1230, 58)))

    def dismantle_skill_exp_double(self):
        self.touch_img("技能_双倍兑换.png")

    def dismantle_skill_exp(self):
        self.touch_img("技能_兑换.png")

    def dismantle_skill_paper(self):
        self.touch_img("技能_编写.png")





