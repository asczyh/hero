from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import settings


def get_driver():
    """初始化并返回 Appium Driver"""
    options = UiAutomator2Options()
    options.platform_name = settings.PLATFORM_NAME
    options.platform_version = settings.PLATFORM_VERSION
    options.device_name = settings.DEVICE_NAME
    options.app_package = settings.APP_PACKAGE
    options.app_activity = settings.APP_ACTIVITY
    options.no_reset = settings.NO_RESET
    options.new_command_timeout = settings.NEW_COMMAND_TIMEOUT
    options.automation_name = settings.AUTOMATION_NAME

    driver = webdriver.Remote(settings.APPIUM_SERVER_URL, options=options)

    # 打印日志信息
    print("appPackage:", driver.capabilities.get('appPackage'))
    print("appActivity:", driver.capabilities.get('appActivity'))

    driver.implicitly_wait(settings.IMPLICITLY_WAIT)
    return driver