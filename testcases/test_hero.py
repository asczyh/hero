from pages.gm_page import GmPage
from utils import *
from airtest.core.api import swipe, find_all, sleep
from common.device import connect_mumu
from config import settings
from pages.hero_page import HeroPage
from utils import rc


class TestHero:
    def test_star(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        gm_page.input("清空英雄", 1)
        gm_page.input("恺撒",6)

        hero_page.choose_hero("恺撒.png", 3)
        gm_page.exit()


    def test_1(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)


        #恺撒_3红.png