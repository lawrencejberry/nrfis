import csv

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base, Basement, StrongFloor, SteelFrame
from database.metadata import (
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)

DATABASE_URL = "postgresql+psycopg2://postgres:@localhost/timescaletest"
db = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

Base.metadata.create_all(db)

session = SessionLocal()

with open(
    "backend/database/test_data/basement_fbg_metadata.csv", encoding="utf-8-sig"
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(BasementMetadata(**row))

with open(
    "backend/database/test_data/strong_floor_fbg_metadata.csv", encoding="utf-8-sig",
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(StrongFloorMetadata(**row))

with open(
    "backend/database/test_data/steel_frame_fbg_metadata.csv", encoding="utf-8-sig",
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(SteelFrameMetadata(**row))

session.commit()

with db.connect() as conn:
    conn.execute(text("SELECT create_hypertable('basement_fbg', 'timestamp')"))
    conn.execute(text("SELECT create_hypertable('strong_floor_fbg', 'timestamp')"))
    conn.execute(text("SELECT create_hypertable('steel_frame_fbg', 'timestamp')"))

with open(
    "backend/database/test_data/basement_fbg.csv", encoding="utf-8-sig"
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(Basement(**row))

with open(
    "backend/database/test_data/strong_floor_fbg.csv", encoding="utf-8-sig",
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(StrongFloor(**row))

with open(
    "backend/database/test_data/steel_frame_fbg.csv", encoding="utf-8-sig",
) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(SteelFrame(**row))

session.commit()
session.close()

