from sqlalchemy import Column, String, Float, Integer

from . import Base


class BasementMetadata(Base):
    __tablename__ = "basement_fbg_metadata"

    uid = Column(String, primary_key=True)
    channel = Column(Integer)
    index = Column(Integer)
    name = Column(String, unique=True)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    Fg = Column(Float)
    St = Column(Float)
    CTEt = Column(Float)
    CTEs = Column(Float)
    reference_wavelength = Column(Float)
    minimum_wavelength = Column(Float)
    maximum_wavelength = Column(Float)


class StrongFloorMetadata(Base):
    __tablename__ = "strong_floor_fbg_metadata"

    uid = Column(String, primary_key=True)
    channel = Column(Integer)
    index = Column(Integer)
    name = Column(String, unique=True)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    Fg = Column(Float)
    St = Column(Float)
    CTEt = Column(Float)
    CTEs = Column(Float)
    reference_wavelength = Column(Float)
    minimum_wavelength = Column(Float)
    maximum_wavelength = Column(Float)


class SteelFrameMetadata(Base):
    __tablename__ = "steel_frame_fbg_metadata"

    uid = Column(String, primary_key=True)
    channel = Column(Integer)
    index = Column(Integer)
    name = Column(String, unique=True)
    measurement_type = Column(String)
    corresponding_sensor = Column(String)
    initial_wavelength = Column(Float)
    Fg = Column(Float)
    St = Column(Float)
    CTEt = Column(Float)
    CTEs = Column(Float)
    reference_wavelength = Column(Float)
    minimum_wavelength = Column(Float)
    maximum_wavelength = Column(Float)

