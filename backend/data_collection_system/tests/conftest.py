import threading

import pytest

from database_models.utils import make_test_db
from .. import DATABASE_URL, db, Session
from .utils import Mockx30Instrument, Mockx55Instrument
from ..x30.x30_client import x30Client
from ..x55.x55_client import x55Client


make_test_db(DATABASE_URL, db, Session)


@pytest.fixture
def x30_instrument():
    with Mockx30Instrument() as mock_instrument:
        thread = threading.Thread(target=mock_instrument.start)
        thread.daemon = True
        thread.start()
        yield mock_instrument


@pytest.fixture
async def x55_instrument():
    async with Mockx55Instrument() as mock_instrument:
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
    await test_client.connect()
    yield test_client
    await test_client.disconnect()
