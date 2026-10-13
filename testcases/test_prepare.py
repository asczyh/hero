from utils import *
from airtest.core.api import swipe

from config import settings
from pages.hero_page import HeroPage

class TestHero:

    def test_hero(self, device):
        device.start_app(settings.GAME_PACKAGE, settings.GAME_ACTIVITY)
        hero_page = HeroPage(device)

        hero_page.touch_gm()

        hero_page.gm_input("添加金币",1)
        hero_page.gm_input("我要资源",1)
        hero_page.gm_input("技能经验",1)
        hero_page.gm_input("地块解锁", 1)
        hero_page.gm_input("关闭羊皮纸", 1)
        hero_page.gm_input("显示topdebug", 1)
        hero_page.gm_input("行军速度 10倍", 1)
        hero_page.gm_input("我要技能",1)
        hero_page.gm_input("训练基地",1)
        hero_page.gm_input("军事营地",1)
