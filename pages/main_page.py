from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from pages.base_page import BasePage

class MainPage(BasePage):
    # 元素定位器（Locators）
    AGREE_BUTTON_ID = "first_click_ok"
    EXPAND_SEARCH_ID = "expand_search"
    SEARCH_INPUT_ID = "search_src_text"

    def handle_privacy_policy(self):
        """处理用户协议、隐私政策同意（如果有的话）"""
        agree_buttons = self.finds(AppiumBy.ID, self.AGREE_BUTTON_ID)
        if agree_buttons:
            agree_buttons[0].click()
    def click_skip_ad(self):
        self.click_by_text("跳过")
    def click_search_box(self):
        """点击搜索框"""
        self.click(AppiumBy.ID, self.EXPAND_SEARCH_ID)

    def input_search_text(self, text):
        """输入搜索内容并回车"""
        self.send_keys(AppiumBy.ID, self.SEARCH_INPUT_ID, text)
        # 回车确认搜索
        self.driver.press_keycode(AndroidKey.ENTER)