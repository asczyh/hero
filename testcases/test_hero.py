from pages.exp_page import ExpPage
from pages.gm_page import GmPage
from pages.skill_page import SkillPage
from utils import *
from airtest.core.api import swipe, find_all, sleep, keyevent
from common.device import connect_mumu
from config import settings
from pages.hero_page import HeroPage
from utils import rc


class TestHero:
    def _prepare_star(self, device,ast=0):
        hero_page = HeroPage(device)
        #前往英雄界面
        hero_page.back_to_hero()
        #执行升星流程
        hero_page.touch_hero_pos(1)
        hero_page.button_star()
        hero_page.choose_hero("恺撒.png", 3)
        hero_page.touch_img("英雄_升星按钮.png")
        if ast:
            assert hero_page.exist_img("英雄_英雄升星成功.png")
        hero_page.touch_blank()
        if ast:
            hero_page.button_info()
            assert hero_page.exist_img("info_成功获得技能点.png")

    def test_star(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        #GM添加英雄
        gm_page.get_hero(6)
        self._prepare_star(device,1)
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

    def test_skill_exp(self, device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        exp_page=ExpPage(device)
        #准备要分解的英雄
        if not hero_page.exist_img("已执行升星.png"):
            gm_page.get_hero(6)
            self._prepare_star(device)
        hero_page.back_to_hero()
        hero_page.enter_exp_page()

        #测试分解0红英雄所得经验
        exp1=exp_page.read_skill_exp()
        gold1=exp_page.read_gold()
        print(f"最初经验值为{exp1}")
        print(f"最初黄金为{gold1}")
        hero_page.touch_img("英雄_0红.png")
        exp_page.dismantle_skill_exp()
        if hero_page.touch_img_if_present("今日不再提醒.png"):
            hero_page.confirm()
        sleep(2)
        exp2=exp_page.read_skill_exp()
        gold2=exp_page.read_gold()
        print(f"硬币分解0红英雄后经验值为{exp2}")
        assert exp2 == exp1+80

        # 测试分解3红英雄所得经验
        hero_page.touch_img("英雄_3红.png")
        exp_page.dismantle_skill_exp_double()
        if hero_page.touch_img_if_present("今日不再提醒.png"):
            hero_page.confirm()
        sleep(2)
        exp3=exp_page.read_skill_exp()
        gold3=exp_page.read_gold()
        print(f"双倍分解3红英雄后经验值为{exp3}")
        print(f"双倍分解3红英雄后黄金为{gold3}")
        assert exp3 == exp2+640
        assert gold3 == gold2-20

    def test_skill_paper(self, device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        exp_page=ExpPage(device)
        #准备要分解的英雄
        if not hero_page.exist_img("已执行升星.png"):
            gm_page.get_hero(6)
            self._prepare_star(device)
        hero_page.back_to_hero()
        hero_page.enter_paper_page()

        #测试分解0红英雄所得经验
        paper1=exp_page.read_skill_paper()
        print(f"当前技能手稿为{paper1}")
        hero_page.touch_img("英雄_0红.png")
        exp_page.dismantle_skill_paper()
        if hero_page.touch_img_if_present("今日不再提醒.png"):
            hero_page.confirm()
        sleep(2)
        paper2 = exp_page.read_skill_paper()
        print(f"当前技能手稿2为{paper2}")
        assert paper1 == paper2+100

        # 测试分解3红英雄所得经验
        hero_page.touch_img("英雄_3红.png")
        exp_page.dismantle_skill_paper()
        sleep(2)
        paper3 = exp_page.read_skill_paper()
        print(f"当前技能手稿3为{paper3}")
        assert paper3 == paper2+400

    def test_skill_learn(self, device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        exp_page=ExpPage(device)
        skill_page=SkillPage(device)
        #准备gm
        gm_page.open()
        gm_page.input("清空英雄",1)
        gm_page.get_hero(1)
        gm_page.input("清除所有技能,1")
        gm_page.exit()
        #进入技能页面
        hero_page.touch_hero_pos(1)
        hero_page.enter_skill_page()
        #记录开始时exp
        exp1=skill_page.get_exp()
        print(f"最初经验值为{exp1}")
        #强化一级
        skill_page.upgrade_one()
        exp2=skill_page.get_exp()
        print(f"升级一次后经验值为{exp2}")
        assert exp1 == exp2+75
        level1=skill_page.get_level()
        print(f"升级一次后技能等级{level1}")
        assert level1=="2级"
        #强化满级
        skill_page.upgrade_max()
        exp3=skill_page.get_exp()
        print(f"升级满级后经验值为{exp3}")
        assert exp1 == exp3+10275
        level2=skill_page.get_level()
        print(f"升级满级后技能等级为{level2}")
        assert level2=="10级"
        #重置
        skill_page.reset()
        exp4=skill_page.get_exp()
        print(f"重置后经验值为{exp4}")
        assert exp1 == exp4
        level3=skill_page.get_level()
        print(f"重置后技能等级为{level3}")
        assert level3=="1级"



    def test_1(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)
        skill_page=SkillPage(device)

        #记录开始时exp
        exp1=skill_page.get_exp()
        #强化一级
        skill_page.upgrade_one()
        exp2=skill_page.get_exp()
        assert exp1 == exp2+75
        level1=skill_page.get_level()
        print(f"level1={level1}")
        assert level1=="2级"
        #强化满级
        skill_page.upgrade_max()
        exp3=skill_page.get_exp()
        assert exp1 == exp3+10275
        level2=skill_page.get_level()
        print(f"level2={level2}")
        assert level2=="10级"
        #重置
        skill_page.reset()
        exp4=skill_page.get_exp()
        assert exp1 == exp4
        level3=skill_page.get_level()
        print(f"level3={level3}")
        assert level3=="1级"

        print("经验值1234=====================================================")
        print(exp1)
        print(exp2)
        print(exp3)
        print(exp4)

    def test_2(self, device):
        gm_page = GmPage(device)
        hero_page = HeroPage(device)

        skill_page=SkillPage(device)
        #重置
        skill_page.reset()
        exp4=skill_page.get_exp()
        print("经验值1234=====================================================")
        print(exp4)
