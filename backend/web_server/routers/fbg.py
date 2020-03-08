import io
import csv
import json
from enum import Enum
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, Header, HTTPException
from starlette.responses import StreamingResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import Package, Packages
from ..dependencies import get_db
from ..calculations.fbg import Calculations
from ..schemas.fbg import DataType, Schemas, Status

router = APIRouter()


class MediaType(str, Enum):
    JSON = "application/json"
    CSV = "text/csv"


class AveragingWindow(str, Enum):
    milliseconds = "milliseconds"
    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"


class DataCollector:
    def __init__(self, package: Package, data_type: DataType):
        self.package = package
        self.data_type = data_type

    def __call__(
        self,
        session: Session = Depends(get_db),
        averaging_window: AveragingWindow = Query(
            None,
            alias="averaging-window",
            description="Bucket and average samples within a particular time window.",
        ),
        start_time: datetime = Query(
            ...,
            alias="start-time",
            description="ISO 8601 format string representing the start time of the range of data requested.",
            example="2020-02-01T17:28:14.723333",
        ),
        end_time: datetime = Query(
            ...,
            alias="end-time",
            description="ISO 8601 format string representing the end time of the range of data requested.",
            example="2020-02-01T17:28:14.723333",
        ),
    ):
        if start_time > end_time:
            raise HTTPException(
                status_code=422, detail="Start time is later than end time"
            )

        if averaging_window is not None:
            window = func.date_trunc(
                averaging_window.value, self.package.values_table.timestamp
            ).label("timestamp")

            raw_data = (
                session.query(
                    window,
                    *[
                        func.avg(getattr(self.package.values_table, field)).label(field)
                        for field in self.package.values_table.attrs()
                    ],
                )
                .filter(window > start_time)
                .filter(window < end_time)
                .group_by(window)
                .order_by(window)
                .all()
            )
        else:
            raw_data = (
                session.query(self.package.values_table)
                .filter(self.package.values_table.timestamp > start_time)
                .filter(self.package.values_table.timestamp < end_time)
                .all()
            )

        if self.data_type == DataType.raw:
            return raw_data

        metadata = {
            row.uid: row for row in session.query(self.package.metadata_table).all()
        }

        selected_sensors = [
            uid
            for uid, sensor in metadata.items()
            if sensor.type == self.data_type.value
        ]

        return [
            {
                "timestamp": row.timestamp,
                **{
                    (metadata[uid].name or uid): Calculations[self.package][
                        self.data_type
                    ](uid, row, metadata)
                    for uid in selected_sensors
                },
            }
            for row in raw_data
        ]


class ResponseFormatter:
    def __init__(self, schema):
        self.schema = schema

    def __call__(
        self,
        media_type: MediaType = Header(
            MediaType.JSON, description="The format of the response."
        ),
    ):
        if media_type == MediaType.JSON:
            return lambda data: data

        def convert_to_csv(data):
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=self.schema.__fields__)
            writer.writeheader()
            try:  # Row is an object
                validated_data = [self.schema.from_orm(row).dict() for row in data]
            except ValidationError:  # Row is a dict
                validated_data = [self.schema(**row).dict() for row in data]
            writer.writerows(validated_data)
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv")

        return convert_to_csv


@router.get(
    "/basement/raw/",
    response_model=List[Schemas[Packages.basement][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_raw_data(
    data=Depends(DataCollector(Packages.basement, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas[Packages.basement][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    print(Schemas[Packages.basement][DataType.raw])
    return formatter(data)


@router.get(
    "/basement/str/",
    response_model=List[Schemas[Packages.basement][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_str_data(
    data=Depends(DataCollector(Packages.basement, DataType.strain)),
    formatter=Depends(ResponseFormatter(Schemas[Packages.basement][DataType.strain])),
):
    """
    Fetch strain FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/basement/tmp/",
    response_model=List[Schemas[Packages.basement][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_tmp_data(
    data=Depends(DataCollector(Packages.basement, DataType.temperature)),
    formatter=Depends(
        ResponseFormatter(Schemas[Packages.basement][DataType.temperature])
    ),
):
    """
    Fetch temperature FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/raw/",
    response_model=List[Schemas[Packages.strong_floor][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_raw_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas[Packages.strong_floor][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/str/",
    response_model=List[Schemas[Packages.strong_floor][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_str_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.strain)),
    formatter=Depends(
        ResponseFormatter(Schemas[Packages.strong_floor][DataType.strain])
    ),
):
    """
    Fetch strain FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/tmp/",
    response_model=List[Schemas[Packages.strong_floor][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_tmp_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.temperature)),
    formatter=Depends(
        ResponseFormatter(Schemas[Packages.strong_floor][DataType.temperature])
    ),
):
    """
    Fetch temperature FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/raw/",
    response_model=List[Schemas[Packages.steel_frame][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_raw_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas[Packages.steel_frame][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/str/",
    response_model=List[Schemas[Packages.steel_frame][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_str_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.strain)),
    formatter=Depends(
        ResponseFormatter(Schemas[Packages.steel_frame][DataType.strain])
    ),
):
    """
    Fetch strain FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/tmp/",
    response_model=List[Schemas[Packages.steel_frame][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_tmp_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.temperature)),
    formatter=Depends(
        ResponseFormatter(Schemas[Packages.steel_frame][DataType.temperature])
    ),
):
    """
    Fetch temperature FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)


@router.get(
    "/live-status/", response_model=Status,
)
def get_live_status():
    """
    Fetch temperature FBG sensor data from the steel frame for a particular time period.
    """
    with open("/var/status.json") as f:
        status = json.load(f)

    return status
