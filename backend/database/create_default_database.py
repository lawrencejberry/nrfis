import csv

from . import db, Session
from . import Base
from .metadata import (
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)


Base.metadata.create_all(db)

session = Session()

with open("metadata/basement_fbg_metadata.csv", encoding="utf-8-sig") as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(BasementMetadata(**row))

with open("metadata/strong_floor_fbg_metadata.csv", encoding="utf-8-sig") as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(StrongFloorMetadata(**row))

with open("metadata/steel_frame_fbg_metadata.csv", encoding="utf-8-sig") as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        session.add(SteelFrameMetadata(**row))

session.commit()
session.close()
