from datetime import datetime

from pydantic import create_model
from sqlalchemy.inspection import inspect

from .. import basement_package, strong_floor_package, steel_frame_package


def _type(key: str):
    if key == "timestamp":
        return datetime
    return float


class Config:
    orm_mode = True


schemas = {}

for package in (basement_package, strong_floor_package, steel_frame_package):
    schemas[package] = create_model(
        f"{package}",
        **{
            c.key: (_type(c.key), ...)
            for c in inspect(package.values_table).mapper.column_attrs
        },
        __config__=Config,
    )
