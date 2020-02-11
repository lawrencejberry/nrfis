import asyncio
import re
import xml.etree.ElementTree as ET
import string
from itertools import count
from struct import unpack
from enum import IntEnum
from typing import List

from .. import (
    logger,
    Session,
    Base,
    basement_package,
    strong_floor_package,
    steel_frame_package,
)
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
    GetAvailableLaserScanSpeeds,
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
    AvailableLaserScanSpeeds,
    InstrumentUtcDateTime,
    NtpEnabled,
)

HOST = "10.0.0.55"
COMMAND_PORT = 51971
PEAK_STREAMING_PORT = 51972
HEADER_LENGTH = 8


class SetupOptions(IntEnum):
    BASEMENT_AND_FRAME = 0
    STRONG_FLOOR = 1
    BASEMENT = 2
    FRAME = 3

    def __str__(self):
        return self._name_.replace("_", " ")


SETUP_OPTIONS = [str(option) for option in SetupOptions]


class Configuration:
    def __init__(self):
        self.mapping = None  # For every table, for every channel, map an index to an ID
        self.setup = None  # Store the current sensor setup
        self.load(SetupOptions.BASEMENT_AND_FRAME)

    @property
    def packages(self):
        """
        Return the packages associated with the current sensor setup.
        """
        if self.setup == SetupOptions.BASEMENT_AND_FRAME:
            return (
                basement_package,
                steel_frame_package,
            )
        if self.setup == SetupOptions.STRONG_FLOOR:
            return (strong_floor_package,)
        if self.setup == SetupOptions.BASEMENT:
            return (basement_package,)
        if self.setup == SetupOptions.FRAME:
            return (steel_frame_package,)

    def map(self, peaks: List[List[float]], table: Base):
        """
        Map the optical instrument output peaks array of arrays to UID: value pairs for the given database table.
        To turn off the recording of individual sensors change its measurement_type to "off".
        If a sensor can no longer be read at all by the optical instrument, remove its row from the metadata table entirely.
        """
        mapped_peaks = {}
        for uid, metadata in self.mapping[table].items():
            channel = metadata["channel"]
            index = metadata["index"]
            recording = metadata["recording"]
            minimum_wavelength = metadata["minimum_wavelength"]
            maximum_wavelength = metadata["maximum_wavelength"]

            # Skip disabled sensors
            if not recording:
                continue

            # Search peaks[channel] array for a matching sensor
            # Readings may accidentally be dropped, but extra readings cannot be added, therefore
            # the sensor's actual index can only be equal to or lower than the expected index
            for measurement in peaks[channel][index::-1]:  # Start at the expected index
                if minimum_wavelength < measurement < maximum_wavelength:
                    mapped_peaks[uid] = measurement
                    break
                # Otherwise the sensor has been dropped or is out-of-band, so ignore

        return mapped_peaks

    def load(self, setup: SetupOptions):
        """
        Load a new configuration from database metadata tables.
        """
        self.setup = setup
        self.mapping = {}  # {"Basement": {"A1":{"channel":1, "index":1, "coeffs..."}}}

        # Load in metadata from tables to mapping
        session = Session()
        for package in self.packages:
            self.mapping[package.values_table] = {
                row.uid: row._asdict()["data"]
                for row in session.query(package.metadata_table).all()
            }
        session.close()

        logger.info("Loaded configuration from database")

    def parse(self, config_file):
        """
        Parse and save a configuration to the database metadata tables.
        Any sensor UIDs or names referenced in the file that exist will be updated,
        but additional UIDs or names in the file will be ignored. It is therefore
        safe to update just Basement metadata table from a combined config file, whilst
        it is also safe to update both the Basement and Steel Frame metadata tables simultaneously.
        """
        session = Session()

        root = ET.parse(config_file).getroot()

        for package in self.packages:
            # Data associated with a UID
            for sensor in root.iter("SensorConfiguration"):
                uid = re.search("[^_]{1,3}$", sensor.find("Name").text)[0]
                reference_wavelength = sensor.find("Reference").text
                minimum_wavelength = sensor.find("WavelengthMinimum").text
                maximum_wavelength = sensor.find("WavelengthMaximum").text

                channel = string.ascii_uppercase.index(uid[0])
                index = int(uid[1:])

                data = {
                    "channel": channel,
                    "index": index,
                    "reference_wavelength": reference_wavelength,
                    "minimum_wavelength": minimum_wavelength,
                    "maximum_wavelength": maximum_wavelength,
                }
                if data:
                    session.query(package.metadata_table).filter(
                        package.metadata_table.uid == uid
                    ).update(data)

            # Data associated with a sensor name
            for transducer in root.iter("Transducer"):
                name = transducer.find("ID").text
                data = {}
                for constant in transducer.iter("TransducerConstant"):
                    constant_name = constant.find("Name").text
                    constant_value = constant.find("Value").text

                    if constant_name.startswith("FBG") and constant_name.endswith("0"):
                        uid = re.search("_([^;]*)_", constant_name)[1]
                        session.query(package.metadata_table).filter(
                            package.metadata_table.uid == uid
                        ).update({"initial_wavelength": constant_value})
                    elif constant_name in ("Fg", "St", "CTEs", "CTEt"):
                        data[constant_name] = constant_value

                if data:
                    session.query(package.metadata_table).filter(
                        package.metadata_table.name == name
                    ).update(data)

        session.commit()
        session.close()

        logger.info("Uploaded new configuration file to database")

        self.load(self.setup)  # Load the newly parsed config file


class Connection:
    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.reading = asyncio.Condition()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logger.info("%s connected to %s:%d", self.name, self.host, self.port)

    async def disconnect(self):
        if self.writer is not None:
            self.writer.close()
            await self.writer.wait_closed()
            logger.info("%s disconnected from %s:%d", self.name, self.host, self.port)

    async def read(self) -> bytes:
        async with self.reading:
            header = await self.reader.readexactly(HEADER_LENGTH)
            status = not unpack("<?", header[0:1])[0]  # True if successful
            message_size = unpack("<H", header[2:4])[0]
            content_size = unpack("<I", header[4:8])[0]
            response = await self.reader.readexactly(message_size + content_size)
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
        self.sampling_rate = None
        self.available_sampling_rates = [None]
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
        self.configuration = Configuration()

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
            await self.command.execute(GetInstrumentName())
        ).content

        self.firmware_version = FirmwareVersion(
            await self.command.execute(GetFirmwareVersion())
        ).content

        self.is_ready = Ready(await self.command.execute(IsReady())).content

        self.dut_channel_count = DutChannelCount(
            await self.command.execute(GetDutChannelCount())
        ).content

        self.sampling_rate = LaserScanSpeed(
            await self.command.execute(GetLaserScanSpeed())
        ).content

        self.available_sampling_rates = AvailableLaserScanSpeeds(
            await self.command.execute(GetAvailableLaserScanSpeeds())
        ).content

        self.peak_data_streaming_status = PeakDataStreamingStatus(
            await self.command.execute(GetPeakDataStreamingStatus())
        ).content

        self.peak_data_streaming_divider = PeakDataStreamingDivider(
            await self.command.execute(GetPeakDataStreamingDivider())
        ).content

        self.peak_data_streaming_available_buffer = PeakDataStreamingAvailableBuffer(
            await self.command.execute(GetPeakDataStreamingAvailableBuffer())
        ).content

        self.instrument_time = InstrumentUtcDateTime(
            await self.command.execute(GetInstrumentUtcDateTime())
        ).content

        self.ntp_enabled = NtpEnabled(
            await self.command.execute(GetNtpEnabled())
        ).content

    async def update_sampling_rate(self, sampling_rate: int) -> bool:
        status = Response(
            await self.command.execute(SetLaserScanSpeed(speed=sampling_rate))
        ).status
        if status:  # If successful
            self.sampling_rate = sampling_rate
        return status

    async def update_setup(self, setup: SetupOptions) -> bool:
        self.configuration.load(setup)
        return True

    async def stream(self):
        await self.peaks.connect()
        self.streaming = Response(
            await self.command.execute(EnablePeakDataStreaming())
        ).status
        logger.info("%s started streaming", self.name)

        while self.streaming:
            yield Peaks(await self.peaks.read())

        # Disconnect and clear out the remaining data from the buffer
        await self.command.execute(DisablePeakDataStreaming())

        buffer = bytes()
        while True:
            try:
                data = await asyncio.wait_for(self.peaks.reader.read(), timeout=0.1)
            except asyncio.TimeoutError:
                break
            buffer += data

        await self.peaks.disconnect()

        # Log the size of the unprocessed buffer
        logger.info(
            "%s finished streaming with %d unproccessed bytes in the TCP buffer",
            self.name,
            len(buffer),
        )

    async def record(self):
        session = Session()
        sample_count = 0

        async for response in self.stream():
            for table in self.configuration.mapping:
                peaks = self.configuration.map(response.content, table)
                session.add(table(timestamp=response.timestamp, **peaks))

            # Commit after every 2000 samples
            sample_count += 1
            if sample_count > 2000:
                session.commit()
                sample_count = 0

        session.commit()
        session.close()
