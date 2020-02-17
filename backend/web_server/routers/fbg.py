from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel, create_model
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from .. import Package, basement_package, strong_floor_package, steel_frame_package
from ..dependencies import get_db
from ..calculations import (
    calculate_uncompensated_strain,
    calculate_temperature_compensated_strain,
)
from ..schemas.fbg import schemas


class DataType(str, Enum):
    raw_wavelength = "raw-wavelength"
    uncompensated_strain = "uncompensated-strain"
    temperature_compensated_strain = "temperature-compensated-strain"


router = APIRouter()


class RawDataCollector:
    def __init__(self, package: Package):
        self.package = package

    def __call__(
        self,
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
        if start_time > end_time:
            raise HTTPException(
                status_code=422, detail="Start time is later than end time"
            )

        raw_data = (
            session.query(self.package.values_table)
            .filter(self.package.values_table.timestamp > start_time)
            .filter(self.package.values_table.timestamp < end_time)
            .all()
        )
        # return raw_data

        metadata = {
            row.uid: row._asdict()["data"]
            for row in session.query(self.package.metadata_table).all()
        }

        return raw_data


@router.get("/basement/", response_model=List[schemas[basement_package]])
def get_basement_data(
    raw_data: List[basement_package.values_table] = Depends(
        RawDataCollector(basement_package)
    ),
):
    """
    Fetch FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return raw_data


@router.get("/strong-floor/", response_model=List[schemas[strong_floor_package]])
def get_strong_floor_data(
    raw_data: List[strong_floor_package.values_table] = Depends(
        RawDataCollector(strong_floor_package)
    ),
):
    """
    Fetch FBG sensor data from the strong floor for a particular time period.
    """
    return raw_data


@router.get("/steel-frame/", response_model=List[schemas[steel_frame_package]])
def get_steel_frame_data(
    raw_data: List[steel_frame_package.values_table] = Depends(
        RawDataCollector(steel_frame_package)
    ),
):
    """
    Fetch FBG sensor data from the steel frame for a particular time period.
    """
    return raw_data
