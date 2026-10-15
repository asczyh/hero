from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
from utils import *
from airtest.core.api import swipe, sleep
from config import settings
from pages.hero_page import HeroPage

class TestPrepare:
    def test_gm(self, device):
        page = HeroPage(device)
        # 准备 GM
        page.touch_gm()
        page.gm_input("添加金币",1)
        page.gm_input("我要资源",1)
        page.gm_input("技能经验",1)
        page.gm_input("地块解锁", 1)
        page.gm_input("关闭羊皮纸", 1)
        page.gm_input("显示topdebug", 1)
        page.gm_input("行军速度 10倍", 1)
        page.gm_input("我要技能",1)
        page.gm_input("训练基地",1)
        page.gm_input("军事营地",1)
        page.touch_img("退出GM.png")
        page.touch_blank()

    def test_barracks(self, device):
        page = HeroPage(device)
        # 建造军营
        page.touch_img("地图_主城.png")
        page.touch_img("市中心按钮.png")
        page.touch_img("市中心_新建设施图标.png")
        page.touch_img("建造_军营.png")
        page.touch_img("建造_前往建造.png")
        page.touch_img("确定.png")
        page.touch_blank()

    def test_facilities(self, device):
        page = HeroPage(device)
        # 建造军营设施
        page.touch_img("地图_主城.png")
        page.touch_img("市中心按钮.png")
        page.touch_extreme_img("市中心_军营图标.png", "top")  # 点击最上方的军营图标
        page.wait_img("前往.png")
        page.device.touch(rc(1500,680))  #点击第一个前往按钮，跳转到马厩
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.wait_img("前往.png")
        page.device.touch(rc(1500,750))  #点击第二个前往按钮
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.device.swipe(rc(1200,680), rc(1200,780))
        page.wait_img("前往.png")
        page.device.touch(rc(1500,722))  #点击第三个前往按钮
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.device.swipe(rc(1200,780), rc(1200,680))
        page.wait_img("前往.png")
        page.device.touch(rc(1500,780))  #点击第四个前往按钮
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")
        page.device.touch(rc(413, 194))


