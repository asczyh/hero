from idlelib.debugobj import dispatch
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from airtest.core.api import *
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find(self, by, value):
        """查找单个元素"""
        return self.driver.find_element(by, value)

    def finds(self, by, value):
        """查找多个元素"""
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        """点击元素"""
        self.find(by, value).click()
    @dispatch(self,Template)
    def click(self,png):
        """点击图片"""
        touch

    def send_keys(self, by, value, text):
        """输入文本"""
        self.find(by, value).send_keys(text)

    def click_by_text(self, text, timeout=5):
        # UiAutomator2 文本定位
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                        f'new UiSelector().textContains("{text}")'))
        )
        element.click()
        print(f">>> 通过原生定位点击: {text}")
        return True
