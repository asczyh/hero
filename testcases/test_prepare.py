from time import gmtime
from airtest.utils.ffmpeg.ffmpeg_setter import main_print_paths
from time import sleep
from pages.center_page import CenterPage
from pages.hero_page import HeroPage
from pages.gm_page import GmPage
from pages.map_page import MapPage
from utils import rc

class TestPrepare:
    def test_gm(self, device):
        hero_page = HeroPage(device)
        gm_page = GmPage(device)
        # 准备 GM
        gm_page.open()
        gm_page.input("添加金币", 1)
        gm_page.input("我要资源", 1)
        gm_page.input("技能经验", 1)
        gm_page.input("地块解锁", 1)
        gm_page.input("关闭羊皮纸", 1)
        gm_page.input("显示topdebug", 1)
        gm_page.input("行军速度 10倍", 1)
        gm_page.input("我要技能", 1)
        gm_page.input("训练基地", 1)
        gm_page.input("军事营地", 1)
        gm_page.exit()
        hero_page.touch_blank()

    def test_barracks(self, device):
        map_page = MapPage(device)
        center_page = CenterPage(device)

        map_page.enter_center_page()   #进入市中心
        center_page.build()    #点击新建设施按钮
        map_page.build_barracks()   #建造军营

    def test_facilities(self, device):
        map_page = MapPage(device)
        center_page = CenterPage(device)
        #建造军营设施
        map_page.enter_center_page()
        center_page.touch_img_in_region("市中心_军营图标.png",rc(270,150),rc(850,230))
        center_page.touch_img_in_row("前往.png", "市中心_马厩文字.png")
        #center_page.build_facility()
        sleep(1)
        center_page.touch_img_in_region("市中心_军营图标.png",rc(270,150),rc(850,230))
        center_page.touch_img_in_row("前往.png", "市中心_兵工厂文字.png")
        center_page.build_facility()
        sleep(1)
        center_page.touch_img_in_region("市中心_军营图标.png",rc(270,150),rc(850,230))
        center_page.device.swipe(rc(1200,780), rc(1200,680))  # 向上滑动，显示后续设施
        sleep(1)
        center_page.touch_img_in_row("前往.png", "市中心_军事学院文字.png")
        center_page.build_facility()
        sleep(1)
        center_page.touch_img_in_region("市中心_军营图标.png",rc(270,150),rc(850,230))
        center_page.device.swipe(rc(1200,780), rc(1200,680))
        sleep(1)
        center_page.touch_img_in_row("前往.png", "市中心_兵营文字.png")
        center_page.build_facility()

    def test_1(self, device):
        hero_page = HeroPage(device)
        map_page = MapPage(device)
        center_page = CenterPage(device)
        #建造军营设施
        center_page.touch_img_in_region("市中心_军营图标.png",rc(270,150),rc(850,230))




