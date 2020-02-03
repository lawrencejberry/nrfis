import csv
from datetime import datetime
from os import path

import pytest

from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..dependencies import get_db
from database import (
    Base,
    Basement,
    StrongFloor,
    SteelFrame,
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)


DATABASE_URL = "sqlite:///./backend/web_server/tests/.test.db"
db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

if not path.isfile("./backend/web_server/tests/.test.db"):
    Base.metadata.create_all(db)

    initialSession = SessionLocal()

    with open(
        "backend/database/test_data/basement_fbg_metadata.csv", encoding="utf-8-sig"
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            initialSession.add(BasementMetadata(**row))

    with open(
        "backend/database/test_data/strong_floor_fbg_metadata.csv",
        encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            initialSession.add(StrongFloorMetadata(**row))

    with open(
        "backend/database/test_data/steel_frame_fbg_metadata.csv", encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            initialSession.add(SteelFrameMetadata(**row))

    initialSession.commit()

    with open(
        "backend/database/test_data/basement_fbg.csv", encoding="utf-8-sig"
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            initialSession.add(Basement(**row))

    with open(
        "backend/database/test_data/strong_floor_fbg.csv", encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            initialSession.add(StrongFloor(**row))

    with open(
        "backend/database/test_data/steel_frame_fbg.csv", encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            initialSession.add(SteelFrame(**row))

    initialSession.commit()
    initialSession.close()


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
