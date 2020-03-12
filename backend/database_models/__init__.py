from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.inspection import inspect


@as_declarative()
class Base:
    @classmethod
    def attrs(cls):
        primary_key = inspect(cls).primary_key[0].key
        columns = inspect(cls).mapper.column_attrs
        return [c.key for c in columns if c.key != primary_key]


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

    def __str__(self):
        return self.values_table.__name__


class Packages:
    basement = Package(Basement, BasementMetadata)
    strong_floor = Package(StrongFloor, StrongFloorMetadata)
    steel_frame = Package(SteelFrame, SteelFrameMetadata)
