from pages.hero_page import HeroPage
from utils import rc

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
        page.touch_img("地图_主城标志.png")
        page.touch_img("市中心按钮.png")
        page.touch_img("市中心_新建设施图标.png")
        page.touch_img("建造_军营.png")
        page.touch_img("建造_前往建造.png")
        page.touch_img("确定.png")
        page.touch_blank()

    def test_facilities(self, device):
        page = HeroPage(device)
        #建造军营设施
        page.touch_img("地图_主城标志.png")
        page.touch_img("市中心按钮.png")
        page.touch_extreme_img("市中心_军营图标.png", "top")  # 点击最上方的军营图标
        page.touch_img_in_row("前往.png", "市中心_马厩文字.png")
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.touch_img_in_row("前往.png", "市中心_兵工厂文字.png")
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.device.swipe(rc(1200,780), rc(1200,680))  # 向上滑动，显示后续设施
        page.touch_img_in_row("前往.png", "市中心_军事学院文字.png")
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")

        page.touch_extreme_img("市中心_军营图标.png","top")   #点击最上方的军营图标，准备建造下一项建造
        page.device.swipe(rc(1200,780), rc(1200,680))
        page.touch_img_in_row("前往.png", "市中心_兵营文字.png")
        page.touch_img("建造文字按钮.png")
        page.touch_img("加速建造按钮.png")
        page.device.touch(rc(413, 194))




