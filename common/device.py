"""连接 MuMu 安卓模拟器的 Airtest 辅助函数。"""

from airtest.core.api import connect_device

from config import settings


def connect_mumu():
    """使用配置中的 ADB 设备地址连接 Airtest。"""
    return connect_device(settings.AIRTEST_DEVICE_URI)
