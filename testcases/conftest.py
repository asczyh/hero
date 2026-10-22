import pytest
from common.device import connect_mumu

@pytest.fixture(scope="session")
def device():
    """测试会话开始时连接一次 MuMu，并在结束后释放设备。"""
    device = connect_mumu()
    try:
        yield device
    finally:
        device.disconnect()
