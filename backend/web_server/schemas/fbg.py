from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, create_model
from sqlalchemy.inspection import inspect

from .. import Session, Packages, Package


class DataType(str, Enum):
    raw = "raw"
    strain = "str"
    temperature = "tmp"


class Status(BaseModel):
    live: bool
    packages: Tuple[Package]
    sampling_rate: int


class Response(BaseModel):
    timestamp: datetime

    class Config:
        orm_mode = True


def _fields(p, d):
    if d == DataType.raw:
        return {
            c.key: (Optional[float], ...)  # None when measurements are missing
            for c in inspect(p.values_table).mapper.column_attrs
            if c.key != "timestamp"
        }

    session = Session()
    names = [
        (sensor.name or sensor.uid)
        for sensor in session.query(p.metadata_table).all()
        if sensor.type == d.value
    ]
    session.close()

    return {
        name: (Optional[float], ...) for name in names
    }  # None when measurements are missing


Schemas = {}

for package in (Packages.basement, Packages.strong_floor, Packages.steel_frame):
    Schemas[package] = {
        data_type: create_model(
            f"{package.values_table.__name__}:{data_type}",
            **_fields(package, data_type),
            __base__=Response,
        )
        for data_type in DataType
    }
