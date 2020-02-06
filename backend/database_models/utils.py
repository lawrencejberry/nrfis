from os import path, remove
import csv
from datetime import datetime
import re

from . import (
    Base,
    Basement,
    StrongFloor,
    SteelFrame,
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)


def make_test_db(DATABASE_URL, db, Session):
    filepath = re.search("///([^;]*)$", DATABASE_URL)[1]

    if path.isfile(filepath):
        remove(filepath)

    session = Session()

    Base.metadata.create_all(db)

    with open(
        "backend/database_models/test_data/basement_fbg_metadata.csv",
        encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["recording"] = row["recording"] == True
            session.add(BasementMetadata(**{k: v for k, v in row.items() if v != ""}))

    with open(
        "backend/database_models/test_data/strong_floor_fbg_metadata.csv",
        encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["recording"] = row["recording"] == True
            session.add(
                StrongFloorMetadata(**{k: v for k, v in row.items() if v != ""})
            )

    with open(
        "backend/database_models/test_data/steel_frame_fbg_metadata.csv",
        encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["recording"] = row["recording"] == True
            session.add(SteelFrameMetadata(**{k: v for k, v in row.items() if v != ""}))

    session.commit()

    with open(
        "backend/database_models/test_data/basement_fbg.csv", encoding="utf-8-sig"
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            session.add(Basement(**{k: v for k, v in row.items() if v != ""}))

    with open(
        "backend/database_models/test_data/strong_floor_fbg.csv", encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            session.add(StrongFloor(**{k: v for k, v in row.items() if v != ""}))

    with open(
        "backend/database_models/test_data/steel_frame_fbg.csv", encoding="utf-8-sig",
    ) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            session.add(SteelFrame(**{k: v for k, v in row.items() if v != ""}))

    session.commit()
    session.close()
