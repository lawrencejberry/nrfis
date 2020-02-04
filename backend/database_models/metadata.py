from sqlalchemy import Column, String, Float

from . import Base


class BasementMetadata(Base):
    __tablename__ = "basement_fbg_metadata"

    id = Column(String, primary_key=True)
    name = Column(String)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    gauge_factor = Column(Float)
    thermo_optic_coefficient = Column(Float)
    location = Column(String)


class StrongFloorMetadata(Base):
    __tablename__ = "strong_floor_fbg_metadata"

    id = Column(String, primary_key=True)
    name = Column(String)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    gauge_factor = Column(Float)
    thermo_optic_coefficient = Column(Float)
    location = Column(String)


class SteelFrameMetadata(Base):
    __tablename__ = "steel_frame_fbg_metadata"

    id = Column(String, primary_key=True)
    name = Column(String)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    gauge_factor = Column(Float)
    thermo_optic_coefficient = Column(Float)
    location = Column(String)
