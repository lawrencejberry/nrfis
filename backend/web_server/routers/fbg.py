import io
import csv
import pickle
from enum import Enum
from datetime import datetime
from typing import List
from asyncio import sleep

from fastapi import APIRouter, Depends, Query, Header, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import StreamingResponse
from starlette.websockets import WebSocket
from websockets.exceptions import ConnectionClosedError
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
                    (metadata[uid].name or uid): Calculations[str(self.package)][
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
    response_model=List[Schemas["Basement"][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_raw_data(
    data=Depends(DataCollector(Packages.basement, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas["Basement"][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/basement/str/",
    response_model=List[Schemas["Basement"][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_str_data(
    data=Depends(DataCollector(Packages.basement, DataType.strain)),
    formatter=Depends(ResponseFormatter(Schemas["Basement"][DataType.strain])),
):
    """
    Fetch strain FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/basement/tmp/",
    response_model=List[Schemas["Basement"][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_basement_tmp_data(
    data=Depends(DataCollector(Packages.basement, DataType.temperature)),
    formatter=Depends(ResponseFormatter(Schemas["Basement"][DataType.temperature])),
):
    """
    Fetch temperature FBG sensor data from the basement raft and perimeter walls for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/raw/",
    response_model=List[Schemas["StrongFloor"][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_raw_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas["StrongFloor"][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/str/",
    response_model=List[Schemas["StrongFloor"][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_str_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.strain)),
    formatter=Depends(ResponseFormatter(Schemas["StrongFloor"][DataType.strain])),
):
    """
    Fetch strain FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/strong-floor/tmp/",
    response_model=List[Schemas["StrongFloor"][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_strong_floor_tmp_data(
    data=Depends(DataCollector(Packages.strong_floor, DataType.temperature)),
    formatter=Depends(ResponseFormatter(Schemas["StrongFloor"][DataType.temperature])),
):
    """
    Fetch temperature FBG sensor data from the strong floor for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/raw/",
    response_model=List[Schemas["SteelFrame"][DataType.raw]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_raw_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.raw)),
    formatter=Depends(ResponseFormatter(Schemas["SteelFrame"][DataType.raw])),
):
    """
    Fetch raw FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/str/",
    response_model=List[Schemas["SteelFrame"][DataType.strain]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_str_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.strain)),
    formatter=Depends(ResponseFormatter(Schemas["SteelFrame"][DataType.strain])),
):
    """
    Fetch strain FBG sensor data from the steel frame for a particular time period.
    """
    return formatter(data)


@router.get(
    "/steel-frame/tmp/",
    response_model=List[Schemas["SteelFrame"][DataType.temperature]],
    responses={
        200: {
            "description": "Return data in JSON or CSV format.",
            "content": {MediaType.JSON: {}, MediaType.CSV: {},},
        },
    },
)
def get_steel_frame_tmp_data(
    data=Depends(DataCollector(Packages.steel_frame, DataType.temperature)),
    formatter=Depends(ResponseFormatter(Schemas["SteelFrame"][DataType.temperature])),
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
    Fetch the status of the data collection system.
    """
    with open("/var/status.pickle", "rb") as f:
        status = pickle.load(f)

    status["packages"] = [str(package) for package in status["packages"]]

    return status


@router.websocket("/live-data/")
async def websocket_endpoint(
    websocket: WebSocket,
    session: Session = Depends(get_db),
    data_type: DataType = Query(
        DataType.raw,
        alias="data-type",
        description="Select the data type of the response.",
    ),
):
    """
    Open a websocket to fetch live data.
    """
    await websocket.accept()

    with open("/var/status.pickle", "rb") as f:
        status = pickle.load(f)

    # Live data is sent at a maximum rate of 10Hz, which is the COMMIT rate
    # of the data collection system
    rate = status["sampling_rate"] if status["sampling_rate"] < 10 else 10

    try:
        previous_timestamp = None
        metadata = {}
        selected_sensors = {}
        while True:
            response = {}
            for package in status["packages"]:
                package_name = str(package)
                row = (
                    session.query(package.values_table)
                    .order_by(package.values_table.timestamp.desc())
                    .first()
                )
                if data_type == DataType.raw:
                    response[package_name] = (
                        Schemas[package_name][DataType.raw].from_orm(row).dict()
                    )
                else:
                    metadata[package_name] = {
                        row.uid: row
                        for row in session.query(package.metadata_table).all()
                    }
                    selected_sensors[package_name] = [
                        uid
                        for uid, sensor in metadata[package_name].items()
                        if sensor.type == data_type.value
                    ]
                    data = {
                        "timestamp": row.timestamp,
                        **{
                            (metadata[package_name][uid].name or uid): Calculations[
                                package_name
                            ][data_type](uid, row, metadata[package_name])
                            for uid in selected_sensors[package_name]
                        },
                    }
                    response[package_name] = Schemas[package_name][data_type](
                        **data
                    ).dict()

                current_timestamp = row.timestamp

            if current_timestamp != previous_timestamp:
                await websocket.send_json(jsonable_encoder(response))

            previous_timestamp = current_timestamp

            # Wait for the next sample to be written to the database
            await sleep(1.0 / rate)
    except HTTPException as e:
        await websocket.send_text(f"Exception occured: {e.detail}")
    except ConnectionClosedError:
        await websocket.close(code=1000)
