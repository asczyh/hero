from pages.gm_page import GmPage
from utils import *
from airtest.core.api import swipe, find_all, sleep, keyevent
from common.device import connect_mumu
from config import settings
from pages.hero_page import HeroPage
from utils import rc


class TestHero:
    def _prepare_star(self, device):
        hero_page = HeroPage(device)
        #前往英雄界面
        hero_page.back_to_hero()
        #执行升星流程
        hero_page.touch_hero_pos(1)
        hero_page.button_star()
        hero_page.choose_hero("恺撒.png", 3)
        hero_page.touch_img("英雄_升星按钮.png")
        assert hero_page.exist_img("英雄_英雄升星成功.png")
        hero_page.touch_blank()
        hero_page.button_info()
        assert hero_page.exist_img("info_成功获得技能点.png")

    def test_star(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        #GM添加英雄
        gm_page.get_hero(6)
        self._prepare_star(device)
        keyevent("BACK")

    def test_allocate_points(self,device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        #如果已经执行过升星获得技能点则直接执行，否则先获得技能点
        hero_page.back_to_hero()
        if not hero_page.exist_img("已执行升星.png"):
            gm_page.get_hero(6)
            self._prepare_star(device)

        hero_page.back_to_hero()
        hero_page.touch_hero_pos(1)
        hero_page.touch_img("info_加点.png")
        hero_page.exist_img("成功进入加点页面.png")
        hero_page.touch_img("info_自动加点.png")
        hero_page.touch_img("确定.png")
        assert hero_page.exist_img("info_加点成功.png")
        hero_page.touch_img("info_洗点.png")
        hero_page.exist_img("提示.png")   #等待确认页面加载
        hero_page.touch_img_if_present("info_免费洗点.png")
        hero_page.touch_img_if_present("20金币确认.png")
        assert hero_page.exist_img("info_成功获得技能点.png")

    def test_skill(self, device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        if not hero_page.exist_img("已执行升星.png"):
            gm_page.get_hero(6)
            self._prepare_star(device)
        hero_page.back_to_hero()
        exp = hero_page.read_skill_exp()
        gold=hero_page.read_text_in_region(rc(1280,20),rc(1395,50))
        hero_page.enter_skill_exp()
        hero_page.touch_img("英雄_0红")
        hero_page.touch_img("技能_双倍兑换.png")
        hero_page.touch_img_if_present("今日不再提醒.png")






    def test_1(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        hero_page.touch_img("英雄_0红.png")
        hero_page.touch_img("技能_双倍兑换.png")
        hero_page.touch_img_if_present("今日不再提醒.png")




    def test_2(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        gold=hero_page.red_gold_skill_page()
        print("金币数量为"+gold)
        silver=hero_page.red_silver_skill_page()
        print("金币数量为"+silver)
