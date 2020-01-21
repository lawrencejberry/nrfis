import asyncio
from struct import pack, unpack
from itertools import count
import logging
import sys


from .x55_protocol import Request, Response, EnablePeakDataStreaming, Peaks

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

HOST = "10.0.0.55"
COMMAND_PORT = 51971
STREAM_PEAKS_PORT = 51972
STREAM_SPECTRA_PORT = 51973
STREAM_SENSORS_PORT = 51974

ACKNOWLEDGEMENT_LENGTH = 8


class Connection:
    def __init__(self, port: int):
        self.port = port
        self.active = False
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, self.port)
        self.active = True
        logger.info(f"Connected to {self.port}")

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.active = False
        logger.info(f"Disconnected from {self.port}")

    async def read(self) -> bytes:
        header = await self.reader.read(ACKNOWLEDGEMENT_LENGTH)
        status = unpack("<B", header[0])
        message_size = unpack("<H", header[2:4])
        content_size = unpack("<I", header[4:8])

        response = await self.reader.read(message_size + content_size)
        message = response[:message_size]
        content = response[message_size : message_size + content_size]

        return status, message, content

    async def execute(self, request: Request) -> bytes:
        self.writer.write(request.serialize())
        return await self.read()


class Connections:
    command = Connection(port=COMMAND_PORT)
    peaks = Connection(port=STREAM_PEAKS_PORT)
    spectra = Connection(port=STREAM_SPECTRA_PORT)
    sensors = Connection(port=STREAM_SENSORS_PORT)


class x55Client:
    """
    Client to interact with an si255 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 2017.09.30 section 6 for details.
    """

    _count = count(1)

    def __init__(self):
        self.name = next(self._count)

        # Connections
        self.conn = Connections()

        # Status information
        # ...

        # Recording and streaming toggles
        self.recording = False
        self.streaming = False

    async def update_status(self):
        pass

    async def stream(self):
        self.conn.peaks.connect()
        status, _, _ = await self.conn.command.execute(EnablePeakDataStreaming)
        self.streaming = status == 0
        logger.info(f"{self.name} started streaming")

        while self.streaming:
            _, _, content = await self.conn.peaks.read()
            yield Peaks(content)

        # Clear out the remaining data and disconnect
        buffer = []
        while True:
            data = self.conn.peaks.reader.read(4096)
            if not data:
                break
            buffer += data

        self.conn.peaks.disconnect()

        # Log the size of the unprocessed buffer
        logger.info(
            f"{self.name} finished streaming with {len(buffer)} unproccessed bytes in the streaming buffer"
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
