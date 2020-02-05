import threading

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data_collection_system
from database_models.utils import make_test_db
from .utils import Mockx30Instrument, Mockx55Instrument
from ..x30.x30_client import x30Client
from ..x55.x55_client import x55Client

# Create SQLite database engine
DATABASE_URL = "sqlite:///./backend/data_collection_system/tests/.test.db"
db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

make_test_db(DATABASE_URL, db, SessionLocal)

# Monkeypatch database
@pytest.fixture(autouse=True)
def override_db(monkeypatch):
    monkeypatch.setattr(data_collection_system, "DATABASE_URL", DATABASE_URL)
    monkeypatch.setattr(data_collection_system, "db", db)
    monkeypatch.setattr(data_collection_system, "Session", SessionLocal)


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
