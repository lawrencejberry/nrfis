from datetime import datetime, timezone
from typing import List, Tuple
from itertools import accumulate
from struct import pack, unpack

from pydantic import BaseModel


# Requests
class Request(BaseModel):
    _serializers = {
        datetime: lambda x: x.strftime(f"%m.%d.%H.%M.%y").encode("ascii"),
        bool: lambda x: str(int(x)).encode("ascii"),
    }
    _default_serializer = lambda self, x: str(x).encode("ascii")

    def serialize(self):
        request_option = pack("<B", 0)
        pad_byte = pack("<x")

        command = b"#%b" % (self.__class__.__name__).encode("ascii")
        arguments = b" ".join(
            [
                self._serializers.get(
                    self.__fields__[k].type_, self._default_serializer
                )(v)
                for k, v in self.dict().items()
            ]
        )

        command_size = pack("<H", len(command))
        arguments_size = pack("<I", len(arguments))

        request = b"".join(
            (request_option, pad_byte, command_size, arguments_size, command, arguments)
        )
        return request


class GetFirmwareVersion(Request):
    pass


class GetInstrumentName(Request):
    pass


class IsReady(Request):
    pass


class GetDutChannelCount(Request):
    pass


class GetPeaks(Request):
    pass


class EnablePeakDataStreaming(Request):
    pass


class DisablePeakDataStreaming(Request):
    pass


class GetPeakDataStreamingStatus(Request):
    pass


class GetPeakDataStreamingDivider(Request):
    pass


class SetPeakDataStreamingDivider(Request):
    divider: int


class GetPeakDataStreamingAvailableBuffer(Request):
    pass


class GetLaserScanSpeed(Request):
    pass


class SetLaserScanSpeed(Request):
    speed: int


class GetAvailableLaserScanSpeeds(Request):
    pass


class GetInstrumentUtcDateTime(Request):
    pass


class GetNtpEnabled(Request):
    pass


class GetNtpServer(Request):
    pass


# Responses
class Response(BaseModel):
    status: bool
    message: str
    content: bytes

    def __init__(self, response: Tuple[bool, bytes, bytes]):
        status, message, content = response
        try:
            super().__init__(status=status, message=message, **self.parse(content))
        except:
            raise ValueError("Could not parse response")

    def parse(self, content: bytes):
        return {"content": content}


class FirmwareVersion(Response):
    content: str

    def parse(self, content: bytes):
        version = content.decode("ascii")

        return {"content": version}


class InstrumentName(Response):
    content: str

    def parse(self, content: bytes):
        name = content.decode("ascii")

        return {"content": name}


class Ready(Response):
    content: bool

    def parse(self, content: bytes):
        ready = unpack("<?", content)[0]

        return {"content": ready}


class DutChannelCount(Response):
    content: int

    def parse(self, content: bytes):
        count = unpack("<I", content)[0]

        return {"content": count}


class Peaks(Response):
    timestamp: datetime
    content: List[List[float]]

    def parse(self, content: bytes):
        timestamp_seconds = unpack("<I", content[16:20])[0]
        timestamp_nanoseconds = unpack("<I", content[20:24])[0]
        num_peaks_per_channel = unpack("<" + 16 * "H", content[24:56])

        cumulative_num_peaks = [0] + list(accumulate(num_peaks_per_channel))
        num_peaks = cumulative_num_peaks[-1]

        raw_peaks = unpack("<" + num_peaks * "d", content[56 : 56 + (num_peaks * 8)])

        timestamp = datetime.fromtimestamp(
            (timestamp_seconds + (timestamp_nanoseconds * 10 ** -9)), timezone.utc
        )
        peaks = [
            raw_peaks[cumulative_num_peaks[i] : cumulative_num_peaks[i + 1]]
            for i in range(16)
        ]

        return {
            "timestamp": timestamp,
            "content": peaks,
        }


class PeakDataStreamingStatus(Response):
    content: bool

    def parse(self, content: bytes):
        status = bool(unpack("<I", content)[0])

        return {"content": status}


class PeakDataStreamingDivider(Response):
    content: int

    def parse(self, content: bytes):
        divider = unpack("<I", content)[0]

        return {"content": divider}


class PeakDataStreamingAvailableBuffer(Response):
    content: int

    def parse(self, content: bytes):
        availability = unpack("<I", content)[0]

        return {"content": availability}


class LaserScanSpeed(Response):
    content: int

    def parse(self, content: bytes):
        speed = unpack("<I", content)[0]

        return {"content": speed}


class AvailableLaserScanSpeeds(Response):
    content: List[int]

    def parse(self, content: bytes):
        available_speeds = unpack("<" + (len(content) // 4) * "I", content)

        return {"content": available_speeds}


class InstrumentUtcDateTime(Response):
    content: datetime

    def parse(self, content: bytes):
        year = unpack("<H", content[:2])[0]
        month = unpack("<H", content[2:4])[0]
        day = unpack("<H", content[4:6])[0]
        hour = unpack("<H", content[6:8])[0]
        minute = unpack("<H", content[8:10])[0]
        second = unpack("<H", content[10:12])[0]

        return {"content": datetime(year, month, day, hour, minute, second)}


class NtpEnabled(Response):
    content: bool

    def parse(self, content: bytes):
        enabled = bool(unpack("<I", content)[0])

        return {"content": enabled}


class NtpServer(Response):
    content: str

    def parse(self, content: bytes):
        ip_address = content.decode("ascii")

        return {"content": ip_address}
