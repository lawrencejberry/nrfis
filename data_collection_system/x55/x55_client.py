import asyncio
import logging
import sys
from itertools import count
from struct import pack, unpack
from enum import IntEnum

from .. import Session
from ..schema import Basement, StrongFloor, SteelFrame
from .x55_protocol import (
    Request,
    GetFirmwareVersion,
    GetInstrumentName,
    IsReady,
    GetDutChannelCount,
    EnablePeakDataStreaming,
    DisablePeakDataStreaming,
    GetPeakDataStreamingStatus,
    GetPeakDataStreamingDivider,
    GetPeakDataStreamingAvailableBuffer,
    GetLaserScanSpeed,
    SetLaserScanSpeed,
    GetInstrumentUtcDateTime,
    GetNtpEnabled,
    Response,
    FirmwareVersion,
    InstrumentName,
    Ready,
    DutChannelCount,
    Peaks,
    PeakDataStreamingStatus,
    PeakDataStreamingDivider,
    PeakDataStreamingAvailableBuffer,
    LaserScanSpeed,
    InstrumentUtcDateTime,
    NtpEnabled,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

HOST = "10.0.0.55"
COMMAND_PORT = 51971
STREAM_PEAKS_PORT = 51972
STREAM_SPECTRA_PORT = 51973
STREAM_SENSORS_PORT = 51974

ACKNOWLEDGEMENT_LENGTH = 8


class Configuration(IntEnum):
    BASEMENT_AND_FRAME = 0
    STRONG_FLOOR = 1


class Connection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.active = False
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.active = True
        logger.info(f"Connected to {self.host}:{self.port}")

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.active = False
        logger.info(f"Disconnected from {self.host}:{self.port}")

    async def read(self) -> bytes:
        header = await self.reader.read(ACKNOWLEDGEMENT_LENGTH)
        status = not unpack("<?", header[0])[0]  # True if successful
        message_size = unpack("<H", header[2:4])[0]
        content_size = unpack("<I", header[4:8])[0]

        response = await self.reader.read(message_size + content_size)
        message = response[:message_size]
        content = response[message_size : message_size + content_size]

        return status, message, content

    async def execute(self, request: Request) -> bytes:
        self.writer.write(request.serialize())
        return await self.read()


class Connections:
    command = Connection(host=HOST, port=COMMAND_PORT)
    peaks = Connection(host=HOST, port=STREAM_PEAKS_PORT)
    spectra = Connection(host=HOST, port=STREAM_SPECTRA_PORT)
    sensors = Connection(host=HOST, port=STREAM_SENSORS_PORT)


class x55Client:
    """
    Client to interact with an si255 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 2017.09.30 section 6 for details.
    """

    _count = count(1)

    def __init__(self):
        self.name = f"x55 Client {next(self._count)}"

        # Connections
        self.host = HOST
        self.conn = Connections()

        # Status information
        self.instrument_name = None
        self.firmware_version = None
        self.is_ready = None
        self.dut_channel_count = None
        self.peak_data_streaming_status = None
        self.peak_data_streaming_divider = None
        self.peak_data_streaming_available_buffer = None
        self.laser_scan_speed = None
        self.instrument_time = None
        self.ntp_enabled = None

        # Recording and streaming toggles
        self.recording = False
        self.streaming = False

        # Configuration setting
        self.configuration = (
            Configuration.BASEMENT_AND_FRAME
        )  # Set to basement and frame by default
        self.sampling_rate = 1000  # Hz

    async def update_status(self):
        self.instrument_name = InstrumentName(
            await self.conn.command.execute(GetInstrumentName)
        ).content

        self.firmware_version = FirmwareVersion(
            await self.conn.command.execute(GetFirmwareVersion)
        ).content

        self.is_ready = Ready(await self.conn.command.execute(IsReady)).content

        self.dut_channel_count = DutChannelCount(
            await self.conn.command.execute(GetDutChannelCount)
        ).content

        self.peak_data_streaming_status = PeakDataStreamingStatus(
            await self.conn.command.execute(GetPeakDataStreamingStatus)
        ).content

        self.peak_data_streaming_divider = PeakDataStreamingDivider(
            await self.conn.command.execute(GetPeakDataStreamingDivider)
        ).content

        self.peak_data_streaming_available_buffer = PeakDataStreamingAvailableBuffer(
            await self.conn.command.execute(GetPeakDataStreamingAvailableBuffer)
        ).content

        self.laser_scan_speed = LaserScanSpeed(
            await self.conn.command.execute(GetLaserScanSpeed)
        ).content

        self.instrument_time = InstrumentUtcDateTime(
            await self.conn.command.execute(GetInstrumentUtcDateTime)
        ).content

        self.ntp_enabled = NtpEnabled(
            await self.conn.command.execute(GetNtpEnabled)
        ).content

    async def update_sampling_rate(self, sampling_rate: int) -> bool:
        status = Response(
            await self.conn.command.execute(SetLaserScanSpeed(speed=sampling_rate))
        ).status
        if status:  # If successful
            self.sampling_rate = sampling_rate
        return status

    async def update_configuration(self, configuration: Configuration) -> bool:
        self.configuration = configuration
        return True

    async def stream(self):
        self.conn.peaks.connect()
        self.streaming = Response(
            await self.conn.command.execute(EnablePeakDataStreaming)
        ).status
        logger.info(f"{self.name} started streaming")

        while self.streaming:
            yield Peaks(await self.conn.peaks.read())

        # Clear out the remaining data and disconnect
        buffer = []
        while True:
            data = self.conn.peaks.reader.read(4096)
            if not data:
                break
            buffer += data

        await self.conn.command.execute(DisablePeakDataStreaming)

        self.conn.peaks.disconnect()

        # Log the size of the unprocessed buffer
        logger.info(
            f"{self.name} finished streaming with {len(buffer)} unproccessed bytes in the streaming buffer"
        )

    async def record(self):
        session = Session()
        sample_count = 0

        async for peaks in self.stream():
            if self.configuration == Configuration.BASEMENT_AND_FRAME:
                basement_sample = Basement(peaks.timestamp, peaks.peaks)
                steel_frame_sample = SteelFrame(peaks.timestamp, peaks.peaks)
                session.add(basement_sample)
                session.add(steel_frame_sample)

            elif self.configuration == Configuration.STRONG_FLOOR:
                strong_floor_sample = StrongFloor(peaks.timestamp, peaks.peaks)
                session.add(strong_floor_sample)

            # Commit after every 2000 samples
            sample_count += 1
            if sample_count > 2000:
                session.commit()
                sample_count = 0

        session.commit()
        session.close()
