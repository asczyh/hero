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





