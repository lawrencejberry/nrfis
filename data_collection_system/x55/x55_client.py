import asyncio
import logging
import sys
from itertools import count
from struct import unpack
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
PEAK_STREAMING_PORT = 51972
HEADER_LENGTH = 8


class Configuration(IntEnum):
    BASEMENT_AND_FRAME = 0
    STRONG_FLOOR = 1


class Connection:
    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
        self.active = False
        self.reader = None
        self.writer = None

    async def connect(self):
        if not self.active:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )
            self.active = True
            logger.info(f"{self.name} connected to {self.host}:{self.port}")

    async def disconnect(self):
        if self.active:
            self.writer.close()
            await self.writer.wait_closed()
            self.active = False
            logger.info(f"{self.name} disconnected from {self.host}:{self.port}")

    async def read(self) -> bytes:
        header = await self.reader.read(HEADER_LENGTH)
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


class x55Client:
    """
    Client to interact with an si255 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 2017.09.30 section 6 for details.
    """

    _count = count(1)

    def __init__(self):
        self.name = f"x55 Client {next(self._count)}"

        # Connection information
        self.host = HOST
        self.command = None
        self.peaks = None
        self.connected = False

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
        self.configuration = Configuration.BASEMENT_AND_FRAME
        self.sampling_rate = 1000  # Hz

    async def connect(self):
        self.command = Connection(self.name, self.host, COMMAND_PORT)
        self.peaks = Connection(self.name, self.host, PEAK_STREAMING_PORT)
        await self.command.connect()
        self.connected = True

    async def disconnect(self):
        await self.command.disconnect()
        await self.peaks.disconnect()
        self.connected = False

    async def update_status(self):
        self.instrument_name = InstrumentName(
            await self.command.execute(GetInstrumentName)
        ).content

        self.firmware_version = FirmwareVersion(
            await self.command.execute(GetFirmwareVersion)
        ).content

        self.is_ready = Ready(await self.command.execute(IsReady)).content

        self.dut_channel_count = DutChannelCount(
            await self.command.execute(GetDutChannelCount)
        ).content

        self.peak_data_streaming_status = PeakDataStreamingStatus(
            await self.command.execute(GetPeakDataStreamingStatus)
        ).content

        self.peak_data_streaming_divider = PeakDataStreamingDivider(
            await self.command.execute(GetPeakDataStreamingDivider)
        ).content

        self.peak_data_streaming_available_buffer = PeakDataStreamingAvailableBuffer(
            await self.command.execute(GetPeakDataStreamingAvailableBuffer)
        ).content

        self.laser_scan_speed = LaserScanSpeed(
            await self.command.execute(GetLaserScanSpeed)
        ).content

        self.instrument_time = InstrumentUtcDateTime(
            await self.command.execute(GetInstrumentUtcDateTime)
        ).content

        self.ntp_enabled = NtpEnabled(await self.command.execute(GetNtpEnabled)).content

    async def update_sampling_rate(self, sampling_rate: int) -> bool:
        status = Response(
            await self.command.execute(SetLaserScanSpeed(speed=sampling_rate))
        ).status
        if status:  # If successful
            self.sampling_rate = sampling_rate
        return status

    async def update_configuration(self, configuration: Configuration) -> bool:
        self.configuration = configuration
        return True

    async def stream(self):
        await self.peaks.connect()
        self.streaming = Response(
            await self.command.execute(EnablePeakDataStreaming)
        ).status
        logger.info(f"{self.name} started streaming")

        while self.streaming:
            yield Peaks(await self.peaks.read())

        # Clear out the remaining data and disconnect
        buffer = []
        while True:
            data = await self.peaks.reader.read(4096)
            if not data:
                break
            buffer += data

        await self.command.execute(DisablePeakDataStreaming)

        await self.peaks.disconnect()

        # Log the size of the unprocessed buffer
        logger.info(
            f"{self.name} finished streaming with {len(buffer)} unproccessed bytes in the streaming buffer"
        )

    async def record(self):
        session = Session()
        sample_count = 0

        async for peaks in self.stream():
            if self.configuration == Configuration.BASEMENT_AND_FRAME:
                session.add(Basement(peaks.timestamp, peaks.content))
                session.add(SteelFrame(peaks.timestamp, peaks.content))

            elif self.configuration == Configuration.STRONG_FLOOR:
                session.add(StrongFloor(peaks.timestamp, peaks.content))

            # Commit after every 2000 samples
            sample_count += 1
            if sample_count > 2000:
                session.commit()
                sample_count = 0

        session.commit()
        session.close()
