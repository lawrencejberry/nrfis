import threading

import pytest

from ..client import x30Client
from .utils import MockServer


@pytest.fixture(autouse=True)
def server():
    with MockServer() as mock_server:
        thread = threading.Thread(target=mock_server.respond)
        thread.daemon = True
        thread.start()
        yield mock_server


@pytest.fixture
async def client():
    test_client = x30Client()
    test_client.host = "127.0.0.1"
    test_client.port = 9500
    await test_client.connect()
    yield test_client
    await test_client.disconnect()
