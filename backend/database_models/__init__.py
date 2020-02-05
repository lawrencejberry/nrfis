from sqlalchemy.ext.declarative import as_declarative
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


class Package:
    def __init__(self, values_table, metadata_table):
        self.values_table = values_table
        self.metadata_table = metadata_table


basement_package = Package(Basement, BasementMetadata)
strong_floor_package = Package(StrongFloor, StrongFloorMetadata)
steel_frame_package = Package(SteelFrame, SteelFrameMetadata)
