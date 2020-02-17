from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.inspection import inspect


@as_declarative()
class Base:
    def _asdict(self):
        columns = inspect(self).mapper.column_attrs
        return {c.key: getattr(self, c.key) for c in columns}


from .basement import Basement
from .strong_floor import StrongFloor
from .steel_frame import SteelFrame
from .metadata import (
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)


class Package:
    def __init__(self, values_table, metadata_table):
        self.values_table = values_table
        self.metadata_table = metadata_table


class Packages:
    basement = Package(Basement, BasementMetadata)
    strong_floor = Package(StrongFloor, StrongFloorMetadata)
    steel_frame = Package(SteelFrame, SteelFrameMetadata)

