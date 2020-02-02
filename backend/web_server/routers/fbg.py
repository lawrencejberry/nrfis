from enum import Enum
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from .. import Session as SessionLocal
from .. import BasementSample, StrongFloorSample, SteelFrameSample
from ..schemas import BasementResponse, StrongFloorResponse, SteelFrameResponse


class DataType(str, Enum):
    raw_wavelength = "raw-wavelength"
    uncompensated_strain = "uncompensated-strain"
    temperature_compensated_strain = "temperature-compensated-strain"


router = APIRouter()

# Dependencies
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Path operation functions
@router.get("/basement/", response_model=List[BasementResponse])
def get_basement_data(
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested.",
    ),
    start_time: datetime = Query(
        ...,
        alias="start-time",
        description=" ISO 8601 format string representing the start time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    end_time: datetime = Query(
        ...,
        alias="end-time",
        description=" ISO 8601 format string representing the end time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    session: Session = Depends(get_db),
):
    """
    Fetch FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    if start_time > end_time:
        raise HTTPException(
            status_code=422, detail="Start time is later than end time."
        )
    if data_type == DataType.raw_wavelength:
        return (
            session.query(BasementSample)
            .filter(BasementSample.timestamp > start_time)
            .filter(BasementSample.timestamp < end_time)
        ).all()
    else:
        return []


@router.get("/strong-floor/", response_model=List[StrongFloorResponse])
def get_strong_floor_data(
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested.",
    ),
    start_time: datetime = Query(
        ...,
        alias="start-time",
        description=" ISO 8601 format string representing the start time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    end_time: datetime = Query(
        ...,
        alias="end-time",
        description=" ISO 8601 format string representing the end time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    session: Session = Depends(get_db),
):
    if start_time > end_time:
        raise HTTPException(
            status_code=422, detail="Start time is later than end time."
        )
    if data_type == DataType.raw_wavelength:
        return (
            session.query(StrongFloorSample)
            .filter(StrongFloorSample.timestamp > start_time)
            .filter(StrongFloorSample.timestamp < end_time)
        ).all()
    else:
        return []


@router.get("/steel-frame/", response_model=List[SteelFrameResponse])
def get_steel_frame_data(
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested.",
    ),
    start_time: datetime = Query(
        ...,
        alias="start-time",
        description=" ISO 8601 format string representing the start time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    end_time: datetime = Query(
        ...,
        alias="end-time",
        description=" ISO 8601 format string representing the end time of the range of data requested.",
        example="2020-02-01T17:28:14.723333",
    ),
    session: Session = Depends(get_db),
):
    if start_time > end_time:
        raise HTTPException(
            status_code=422, detail="Start time is later than end time."
        )
    if data_type == DataType.raw_wavelength:
        return (
            session.query(SteelFrameSample)
            .filter(SteelFrameSample.timestamp > start_time)
            .filter(SteelFrameSample.timestamp < end_time)
        ).all()
    else:
        return []
