import pytest

from starlette.testclient import TestClient

from database_models.utils import make_test_db
from .. import DATABASE_URL, db, Session

make_test_db(DATABASE_URL, db, Session)

from ..main import app


@pytest.fixture
def client():
    return TestClient(app)
