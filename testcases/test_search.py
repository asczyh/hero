from config import settings
from pages.main_page import MainPage


class TestSearch:
    def test_search_game(self, device):
        """测试搜索功能"""
        device.start_app(settings.BILIBILI_PACKAGE, settings.BILIBILI_ACTIVITY)
        main_page = MainPage(device)

        # 1. 处理隐私协议
        main_page.handle_privacy_policy()
        # 2. 点击搜索框
        main_page.click_search_box()

        # 3. 输入搜索内容并回车
        main_page.input_search_text('Mili')
