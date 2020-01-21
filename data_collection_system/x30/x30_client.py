import asyncio
import struct
from itertools import count
import logging
import sys

from .x30_protocol import (
    Request,
    Response,
    ACKNOWLEDGEMENT_LENGTH,
    STATUS_HEADER_LENGTH,
    GET_DATA,
    SET_STREAMING_DATA,
    DATA,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


class x30Client:
    """
    Client to interact with an sm130 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 1.139 section 4.4.4.5 for details.
    """

    _count = count(1)

    def __init__(self):
        self.name = next(self._count)

        # Default connection information
        self.host = "10.0.0.126"
        self.port = 1852
        self.connected = False

        # I/O
        self.reader = None
        self.writer = None

        # Status information
        self.fs_radix = None
        self.fw_version = None
        self.secondary_fan = None
        self.primary_fan = None
        self.calibration_fault = None
        self.switch_position = None
        self.mux_level = None
        self.triggering_mode = None
        self.operating_mode = None
        self.num_peaks_detected = None
        self.error = None
        self.buffer = None
        self.header_version = None
        self.granularity = None
        self.full_spectrum_start_wvl = None
        self.full_spectrum_end_wvl = None

        # Recording and streaming toggles
        self.recording = False
        self.streaming = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.connected = True
        logger.info(f"{self.name} connected")

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.connected = False
        logger.info(f"{self.name} disconnected")

    async def read(self, override_length: int = None) -> bytes:
        length = int(await self.reader.read(ACKNOWLEDGEMENT_LENGTH))
        if override_length is not None:  # Override message length if provided
            length = override_length
        response = await self.reader.read(length)
        return response

    async def execute(self, request: Request, override_length: int = None) -> bytes:
        self.writer.write(request.serialize())
        return await self.read(override_length)

    async def update_status(self):
        response = await self.execute(GET_DATA())
        status_header = response[:STATUS_HEADER_LENGTH]
        self.fs_radix = status_header[0]
        self.fw_version = status_header[2]
        self.secondary_fan = bool((status_header[3] >> 3) & 1)
        self.primary_fan = bool((status_header[3] >> 4) & 1)
        self.calibration_fault = bool((status_header[3] >> 6) & 1)
        self.switch_position = int(status_header[6] & 3)
        self.mux_level = int((status_header[6] >> 1) & 3)
        self.triggering_mode = int((status_header[6] >> 4) & 3)
        self.operating_mode = int((status_header[6] >> 6) & 3)
        self.num_peaks_detected = ", ".join(
            [str(num) for num in struct.unpack("<HHHH", status_header[16:24])]
        )
        self.error = status_header[47]
        self.buffer = status_header[48]
        self.header_version = status_header[49]
        self.granularity = struct.unpack("<L", status_header[72:76])[0]
        self.full_spectrum_start_wvl = struct.unpack("<L", status_header[80:84])[0]
        self.full_spectrum_end_wvl = struct.unpack("<L", status_header[84:88])[0]

    async def stream(self):
        self.streaming = (
            await self.execute(SET_STREAMING_DATA(val=True))
        ) == b"Streaming data enabled.\n"
        await self.execute(GET_DATA())
        logger.info(f"{self.name} started streaming")

        while self.streaming:
            response = await self.read()
            while (
                response[-8:] != b"XXXXXXXX"
            ):  # Continue reading in until 8 Xs have been received
                response += await self.reader.read(1)
            yield DATA(response)

        exit_response = await self.execute(SET_STREAMING_DATA(val=False))
        # Stop streaming after 8 Zs have been received
        while exit_response[-8:] != b"ZZZZZZZZ":
            exit_response += await self.reader.read(1024)
        # logger.info the length of the exit response, which shows how much data we haven't processed since stopping streaming
        logger.info(
            f"{self.name} finished streaming. {len(exit_response)} bytes in the streaming buffer were not processed."
        )

    # async def record(self):
    #     db = create_engine(
    #         "postgresql+psycopg2://postgres:@localhost/timescaletest", echo=False
    #     )
    #     Session = sessionmaker(db)
    #     session = Session()

    #     i = 0
    #     async for response in self.stream():
    #         channel_1_peaks_in_nm = [
    #             peak / response.granularity for peak in response.channel_1_peaks
    #         ]
    #         channel_2_peaks_in_nm = [
    #             peak / response.granularity for peak in response.channel_2_peaks
    #         ]
    #         channel_3_peaks_in_nm = [
    #             peak / response.granularity for peak in response.channel_3_peaks
    #         ]
    #         channel_4_peaks_in_nm = [
    #             peak / response.granularity for peak in response.channel_4_peaks
    #         ]

    #         # Now store data in database
    #         # Create
    #         entry = TestTable(sensor_1=channel_1_peaks_in_nm[0], sensor_2=0.0)
    #         session.add(entry)
    #         i += 1
    #         if i > 2000:
    #             session.flush()
    #             i = 0

    #     session.flush()
    #     session.commit()
