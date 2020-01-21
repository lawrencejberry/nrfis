from datetime import datetime, timezone
from typing import List
from itertools import accumulate
from struct import pack, unpack

from pydantic import BaseModel


# Requests
class Request(BaseModel):
    _serializers = {
        datetime: lambda x: x.strftime(f"%m.%d.%H.%M.%y").encode("ascii"),
        bool: lambda x: str(int(x)).encode("ascii"),
    }
    _default_serializer = lambda x: str(x).encode("ascii")

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

        return b" ".join(
            (request_option, pad_byte, command_size, arguments_size, command, arguments)
        )


class GetPeaks(Request):
    pass


class EnablePeakDataStreaming(Request):
    pass


class DisablePeakDataStreaming(Request):
    pass


class GetPeakDataStreamingStatus(Request):
    pass


# Responses
class Response(BaseModel):
    def __init__(self, content: bytes):
        try:
            super().__init__(**self.parse(content))
        except:
            raise ValueError("Could not parse response")


class Peaks(Response):
    timestamp: datetime
    peaks: List[List[float]]

    def parse(self, content: bytes):
        timestamp_seconds = unpack("<I", content[16:20])
        timestamp_nanoseconds = unpack("<I", content[20:24])
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
            "peaks": peaks,
        }

