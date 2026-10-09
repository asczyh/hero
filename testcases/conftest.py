import pytest
from common.device import get_driver

@pytest.fixture(scope="function")
def driver():
    """每个测试用例前启动驱动，结束后退出"""
    driver = get_driver()
    # 激活 App
    driver.activate_app('tv.danmaku.bili')
    yield driver
    # 用例结束后退出
    driver.quit()