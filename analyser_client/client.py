import asyncio
import struct

from protocol import Request, GET_DATA, SET_STREAMING_DATA


class x30Client:
    """
    Client to interact with an sm130 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 1.139 section 4.4.4.5 for details.
    """

    ACKNOWLEDGEMENT_LENGTH = 10  # bytes
    STATUS_HEADER_LENGTH = 88  # bytes

    def __init__(self):
        # Connection information
        self.host = "10.0.0.126"
        self.port = 1852
        self.connected = False

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

        # Streaming toggle
        self.streaming = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.connected = True

    async def disconnect(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.connected = False

    async def read(self, override_length: int = None) -> bytes:
        length = int(await self.reader.read(self.ACKNOWLEDGEMENT_LENGTH))
        if override_length is not None:  # Override message length if provided
            length = override_length
        response = await self.reader.read(length)
        return response

    async def execute(self, request: Request, override_length: int = None) -> bytes:
        self.writer.write(request.serialize())
        return await self.read(override_length)

    async def update_status(self):
        response = await self.execute(GET_DATA())
        status_header = response[:88]
        self.fs_radix = status_header[0]
        self.fw_version = status_header[2]
        self.secondary_fan = bool((status_header[3] >> 3) & 1)
        self.primary_fan = bool((status_header[3] >> 4) & 1)
        self.calibration_fault = bool((status_header[3] >> 6) & 1)
        self.switch_position = int(status_header[6] & 3)
        self.mux_level = int((status_header[6] >> 1) & 3)
        self.triggering_mode = int((status_header[6] >> 4) & 3)
        self.operating_mode = int((status_header[6] >> 6) & 3)
        self.num_peaks_detected = status_header[16:24].decode("ascii")
        self.error = status_header[47]
        self.buffer = status_header[48]
        self.header_version = status_header[49]
        self.granularity = struct.unpack("<L", status_header[72:76])[0]
        self.full_spectrum_start_wvl = struct.unpack("<L", status_header[80:84])
        self.full_spectrum_end_wvl = struct.unpack("<L", status_header[84:88])

    async def stream_data(self):
        self.streaming = await bool(int(self.execute(SET_STREAMING_DATA(val=True))))
        await self.execute(GET_DATA())
        while self.streaming:
            response = await self.read()
            # Then process the response
        await self.execute(SET_STREAMING_DATA(val=False))
