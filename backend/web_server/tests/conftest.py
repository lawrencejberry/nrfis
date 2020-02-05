import pytest

from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_models.utils import make_test_db
from ..main import app
from ..dependencies import get_db


# Create SQLite database engine
DATABASE_URL = "sqlite:///./backend/web_server/tests/.test.db"
db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

make_test_db(DATABASE_URL, db, SessionLocal)


def override_get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)
