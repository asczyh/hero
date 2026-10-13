import pytest
from common.device import connect_mumu

@pytest.fixture(scope="session")
def device():
    """Connect to MuMu once for the test session and release it afterward."""
    device = connect_mumu()
    try:
        yield device
    finally:
        device.disconnect()
