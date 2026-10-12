import pytest
from airtest.core.api import connect_device
from common.device import get_driver

@pytest.fixture(scope="function")
def driver():
    """每个测试用例前启动驱动，结束后退出"""
    driver = get_driver()
    # Airtest and Appium must control the same Android device.
    udid = driver.capabilities.get("udid") or driver.capabilities.get("appium:udid")
    if not udid:
        driver.quit()
        raise RuntimeError(
            "Appium session did not return a device udid; "
            "Airtest cannot connect to the same emulator."
        )
    try:
        connect_device(f"Android://127.0.0.1:5037/{udid}")
    except Exception:
        driver.quit()
        raise


    # 激活 App
    #driver.activate_app('tv.danmaku.bili')
    yield driver
    # 用例结束后退出
    driver.quit()
