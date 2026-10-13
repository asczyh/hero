from utils import *
from airtest.core.api import swipe

from config import settings
from pages.hero_page import HeroPage

class TestHero:

    def test_hero(self, device):
        device.start_app(settings.GAME_PACKAGE, settings.GAME_ACTIVITY)
        hero_page = HeroPage(device)

        # hero_page.touch_gm()
        # swipe(
        #     rc(250,100),
        #     rc(250, 200),
        #     duration=0.5,
        # )
        hero_page.gm_input("萨拉丁",1)
