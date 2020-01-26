from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT

from . import Base


class BasementMetadata(Base):
    __tablename__ = "basement_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)


class StrongFloorMetadata(Base):
    __tablename__ = "strong_floor_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)


class SteelFrameMetadata(Base):
    __tablename__ = "steel_frame_fbg_metadata"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    initial_wavelength = Column(DOUBLE_PRECISION)
    gauge_factor = Column(DOUBLE_PRECISION)
    thermo_optic_coefficient = Column(DOUBLE_PRECISION)
    location = Column(TEXT)
