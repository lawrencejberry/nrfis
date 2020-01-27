import threading

import pytest

from .utils import Mockx30Instrument, Mockx55Instrument
from ..x30.x30_client import x30Client
from ..x55.x55_client import x55Client


@pytest.fixture(autouse=True)
def x30_instrument():
    with Mockx30Instrument() as mock_instrument:
        thread = threading.Thread(target=mock_instrument.start)
        thread.daemon = True
        thread.start()
        yield mock_instrument


@pytest.fixture(autouse=True)
def x55_instrument():
    with Mockx55Instrument() as mock_instrument:
        thread_1 = threading.Thread(target=mock_instrument.start)
        thread_2 = threading.Thread(target=mock_instrument.peak_streaming)
        thread_1.daemon = True
        thread_2.daemon = True
        thread_1.start()
        thread_2.start()
        yield mock_instrument


@pytest.fixture
async def x30_client():
    test_client = x30Client()
    test_client.host = "127.0.0.1"
    test_client.port = 9500
    await test_client.connect()
    yield test_client
    await test_client.disconnect()


@pytest.fixture
async def x55_client():
    test_client = x55Client()
    test_client.host = "127.0.0.1"
    await test_client.conn.command.connect()
    yield test_client
    await test_client.conn.command.disconnect()
