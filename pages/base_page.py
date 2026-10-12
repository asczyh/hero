from pathlib import Path

from airtest.core.api import Template, touch
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
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

    def click_img(self, image_path: str | Path):
        """点击 assets/img 中的图片；也接受项目根目录相对路径。"""
        image_path = Path(image_path)
        if not image_path.is_absolute():
            project_root = Path(__file__).resolve().parents[1]
            project_relative_path = project_root / image_path
            image_dir_path = project_root / "assets" / "img" / image_path
            image_path = (
                project_relative_path
                if project_relative_path.is_file()
                else image_dir_path
            )
        if not image_path.is_file():
            raise FileNotFoundError(f"图片模板不存在：{image_path}")
        return touch(Template(str(image_path)))

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
