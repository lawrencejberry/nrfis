import io
import csv
from enum import Enum
from datetime import datetime
from typing import List, Union

from fastapi import APIRouter, Depends, Query, Header, HTTPException
from starlette.responses import StreamingResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import Package, Packages
from ..dependencies import get_db
from ..calculations import Calculations
from ..schemas.fbg import DataType, Schemas

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
    def __init__(self, package: Package):
        self.package = package

    def __call__(
        self,
        session: Session = Depends(get_db),
        data_type: DataType = Query(
            ..., alias="data-type", description="The type of data requested."
        ),
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

        if data_type == DataType.raw:
            return raw_data

        metadata = {
            row.uid: row for row in session.query(self.package.metadata_table).all()
        }

        selected_sensors = [
            uid for uid, sensor in metadata.items() if sensor.type == data_type.value
        ]

        return [
            {
                "timestamp": row.timestamp,
                **{
                    (metadata[uid].name or uid): Calculations[self.package][data_type](
                        uid, row, metadata
                    )
                    for uid in selected_sensors
                },
            }
            for row in raw_data
        ]


class ResponseFormatter:
    def __init__(self, package: Package):
        self.package = package

    def __call__(
        self,
        media_type: MediaType = Header(
            MediaType.JSON, description="The format of the response."
        ),
        data_type: DataType = Query(
            ..., alias="data-type", description="The type of data requested."
        ),
    ):
        if media_type == MediaType.JSON:
            return lambda data: data

        def convert_to_csv(data):
            output = io.StringIO()
            writer = csv.DictWriter(
                output, fieldnames=Schemas[self.package][data_type].__fields__
            )
            writer.writeheader()
            try:  # Row is an object
                validated_data = [
                    Schemas[self.package][data_type].from_orm(row).dict()
                    for row in data
                ]
            except ValidationError:  # Row is a dict
                validated_data = [
                    Schemas[self.package][data_type](**row).dict() for row in data
                ]
            writer.writerows(validated_data)
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv")

        return convert_to_csv


@router.get(
    "/basement/",
    response_model=List[
        Union[tuple(Schemas[Packages.basement][data_type] for data_type in DataType)]
    ],
)
def get_basement_data(
    data=Depends(DataCollector(Packages.basement)),
    formatter=Depends(ResponseFormatter(Packages.basement)),
):
    """
    Fetch FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/",
    response_model=List[
        Union[
            tuple(Schemas[Packages.strong_floor][data_type] for data_type in DataType)
        ]
    ],
)
def get_strong_floor_data(
    data=Depends(DataCollector(Packages.strong_floor)),
    formatter=Depends(ResponseFormatter(Packages.strong_floor)),
):
    """
    Fetch FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/",
    response_model=List[
        Union[tuple(Schemas[Packages.steel_frame][data_type] for data_type in DataType)]
    ],
)
def get_steel_frame_data(
    data=Depends(DataCollector(Packages.steel_frame)),
    formatter=Depends(ResponseFormatter(Packages.steel_frame)),
):
    """
    Fetch FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)
