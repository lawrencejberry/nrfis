from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from .basement import BasementSample
from .strong_floor import StrongFloorSample
from .steel_frame import SteelFrameSample
from .metadata import (
    BasementSensorMetadata,
    StrongFloorSensorMetadata,
    SteelFrameSensorMetadata,
)

# Create database engine
db = create_engine(
    "postgresql+psycopg2://postgres:@localhost/timescaletest", echo=False
)
Session = sessionmaker(db)
