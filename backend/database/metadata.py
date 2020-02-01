from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT

from . import Base


class BasementSensorMetadata(Base):
    __tablename__ = "basement_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    measurement_type = Column(TEXT)
    corresponding_sensor = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)


class StrongFloorSensorMetadata(Base):
    __tablename__ = "strong_floor_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    measurement_type = Column(TEXT)
    corresponding_sensor = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)


class SteelFrameSensorMetadata(Base):
    __tablename__ = "steel_frame_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    measurement_type = Column(TEXT)
    corresponding_sensor = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)
