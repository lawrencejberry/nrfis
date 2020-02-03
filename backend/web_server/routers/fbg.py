from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import (
    Basement,
    StrongFloor,
    SteelFrame,
    BasementMetadata,
    StrongFloorMetadata,
    SteelFrameMetadata,
)
from ..dependencies import get_db
from ..calculations import (
    calculate_uncompensated_strain,
    calculate_temperature_compensated_strain,
)


class DataType(str, Enum):
    raw_wavelength = "raw-wavelength"
    uncompensated_strain = "uncompensated-strain"
    temperature_compensated_strain = "temperature-compensated-strain"


class DataResponse(BaseModel):
    timestamp: datetime
    data: Dict[str, Optional[float]]


router = APIRouter()


def process_data(data_type, raw_data, metadata):
    strain_sensors = [
        sensor
        for sensor, sensor_metadata in metadata.items()
        if sensor_metadata["measurement_type"] == "str"
    ]

    if data_type == DataType.uncompensated_strain:
        return [
            {
                "timestamp": row["timestamp"],
                "data": {
                    metadata[sensor]["name"]: calculate_uncompensated_strain(
                        str_wvl=row["data"][sensor],
                        initial_str_wvl=metadata[sensor]["initial_wavelength"],
                        gauge_factor=metadata[sensor]["gauge_factor"],
                    )
                    for sensor in strain_sensors
                },
            }
            for row in raw_data
        ]

    if data_type == DataType.temperature_compensated_strain:
        return [
            {
                "timestamp": row["timestamp"],
                "data": {
                    metadata[sensor]["name"]: calculate_temperature_compensated_strain(
                        str_wvl=row["data"][sensor],
                        initial_str_wvl=metadata[sensor]["initial_wavelength"],
                        tmp_wvl=row["data"][metadata[sensor]["corresponding_sensor"]],
                        initial_tmp_wvl=metadata[
                            metadata[sensor]["corresponding_sensor"]
                        ]["initial_wavelength"],
                        gauge_factor=metadata[sensor]["gauge_factor"],
                    )
                    for sensor in strain_sensors
                },
            }
            for row in raw_data
        ]


@router.get("/basement/", response_model=List[DataResponse])
def get_basement_data(
    session: Session = Depends(get_db),
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested."
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
):
    """
    Fetch FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    if start_time > end_time:
        raise HTTPException(status_code=422, detail="Start time is later than end time")

    raw_data = [
        row._asdict()
        for row in session.query(Basement)
        .filter(Basement.timestamp > start_time)
        .filter(Basement.timestamp < end_time)
        .all()
    ]

    if data_type == DataType.raw_wavelength:
        return raw_data

    metadata = {
        row.id: row._asdict()["data"] for row in session.query(BasementMetadata).all()
    }

    return process_data(data_type, raw_data, metadata)


@router.get("/strong-floor/", response_model=List)
def get_strong_floor_data(
    session: Session = Depends(get_db),
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested."
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
):
    """
    Fetch FBG sensor data from the strong floor for a particular time period.
    """
    if start_time > end_time:
        raise HTTPException(status_code=422, detail="Start time is later than end time")
    raw_data = [
        row._asdict()
        for row in session.query(StrongFloor)
        .filter(StrongFloor.timestamp > start_time)
        .filter(StrongFloor.timestamp < end_time)
        .all()
    ]

    if data_type == DataType.raw_wavelength:
        return raw_data

    metadata = {
        row.id: row._asdict()["data"]
        for row in session.query(StrongFloorMetadata).all()
    }

    return process_data(data_type, raw_data, metadata)


@router.get("/steel-frame/", response_model=List[DataResponse])
def get_steel_frame_data(
    session: Session = Depends(get_db),
    data_type: DataType = Query(
        ..., alias="data-type", description="The type of data requested."
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
):
    """
    Fetch FBG sensor data from the steel frame for a particular time period.
    """
    if start_time > end_time:
        raise HTTPException(status_code=422, detail="Start time is later than end time")
    raw_data = [
        row._asdict()
        for row in session.query(SteelFrame)
        .filter(SteelFrame.timestamp > start_time)
        .filter(SteelFrame.timestamp < end_time)
        .all()
    ]

    if data_type == DataType.raw_wavelength:
        return raw_data

    metadata = {
        row.id: row._asdict()["data"] for row in session.query(SteelFrameMetadata).all()
    }

    return process_data(data_type, raw_data, metadata)

