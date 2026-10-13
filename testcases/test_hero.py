from utils import *
from airtest.core.api import swipe

from config import settings
from pages import hero_page

class TestHero:

    def test_hero(self, device):
        device.start_app(settings.GAME_PACKAGE, settings.GAME_ACTIVITY)
        heropage = hero_page.HeroPage(device)

        heropage.click_gm()
        swipe(
            rc(250,100),
            rc(250, 200),
            duration=0.5,
        )