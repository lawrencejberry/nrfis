from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect


@as_declarative()
class Base:
    def _asdict(self):
        primary_key = inspect(self.__class__).primary_key[0].key
        columns = inspect(self).mapper.column_attrs
        return {
            primary_key: getattr(self, primary_key),
            "data": {
                c.key: getattr(self, c.key) for c in columns if c.key != primary_key
            },
        }


from .basement import Basement
from .strong_floor import StrongFloor
from .steel_frame import SteelFrame
from .metadata import (
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)

# Create database engine
db = create_engine(
    "postgresql+psycopg2://postgres:@localhost/timescaletest", echo=False
)
Session = sessionmaker(db)
