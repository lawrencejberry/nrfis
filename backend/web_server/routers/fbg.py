from enum import Enum
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from .. import Session


class DataType(str, Enum):
    raw_wavelength = "raw-wavelength"
    uncompensated_strain = "uncompensated-strain"
    temperature_compensated_strain = "temperature-compensated-strain"


class FBGSensorData(BaseModel):
    timestamp: datetime
    data: Dict[str, float]


router = APIRouter()

# Dependencies
async def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


# Path operation functions
@router.get("/basement/", response_model=FBGSensorData)
async def get_basement_data(
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
    session=Depends(get_session),
):
    """
    Fetch FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    if start_time > end_time:
        raise HTTPException(
            status_code=422, detail="Start time is later than end time."
        )
    return {"message": "Hello World"}


@router.get("/strong-floor/")
async def get_strong_floor_data(data_type: DataType):
    return {"message": "Hello World"}


@router.get("/steel-frame/")
async def get_steel_frame_data(data_type: DataType):
    return {"message": "Hello World"}
