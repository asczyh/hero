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
        gm_page.open()
        gm_page.input("清空英雄", 1)
        gm_page.input("恺撒",6)
        gm_page.exit()
        #打开英雄升星界面
        hero_page.touch_hero_pos(1)
        hero_page.button_star()
        #选择素材
        hero_page.choose_hero("恺撒.png", 3)
        gm_page.touch_img("英雄_升星按钮.png")
        assert gm_page.exist_img("英雄_英雄升星成功.png")
        gm_page.touch_blank()


    def test_1(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)

        assert hero_page.exist_img("英雄_升星按钮.png")

        #恺撒_3红.png