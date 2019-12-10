from ipaddress import IPv4Address
from enum import Enum, IntEnum
from datetime import datetime
from typing import Union, List
from itertools import accumulate
from struct import unpack

from pydantic import BaseModel


ACKNOWLEDGEMENT_LENGTH = 10  # bytes
STATUS_HEADER_LENGTH = 88  # bytes


class Channel(IntEnum):
    CHANNEL_1 = 1
    CHANNEL_2 = 2
    CHANNEL_3 = 3
    CHANNEL_4 = 4


class SubChannel(float, Enum):
    CHANNEL_1_1 = 1.1
    CHANNEL_1_2 = 1.2
    CHANNEL_1_3 = 1.3
    CHANNEL_1_4 = 1.4
    CHANNEL_2_1 = 2.1
    CHANNEL_2_2 = 2.2
    CHANNEL_2_3 = 2.3
    CHANNEL_2_4 = 2.4
    CHANNEL_3_1 = 3.1
    CHANNEL_3_2 = 3.2
    CHANNEL_3_3 = 3.3
    CHANNEL_3_4 = 3.4
    CHANNEL_4_1 = 4.1
    CHANNEL_4_2 = 4.2
    CHANNEL_4_3 = 4.3
    CHANNEL_4_4 = 4.4


class NTPServer(IntEnum):
    NTP_SERVER_0 = 0
    NTP_SERVER_1 = 1
    NTP_SERVER_2 = 2
    NTP_SERVER_3 = 3
    NTP_SERVER_4 = 4


class MultiplexerLevel(IntEnum):
    MUX_1 = 1
    MUX_2 = 2
    MUX_4 = 4


class OperatingMode(IntEnum):
    STAND_ALONE = 0
    MASTER = 1
    END_SLAVE = 2
    MIDDLE_SLAVE = 3


class TrigMode(IntEnum):
    UNTRIGGERED = 0
    SW_TRIGGERED = 1
    HW_TRIGGERED = 3


# Requests
class Request(BaseModel):
    _serializers = {
        datetime: lambda x: x.strftime(f"%m.%d.%H.%M.%y").encode("ascii"),
        bool: lambda x: str(int(x)).encode("ascii"),
    }
    _default_serializer = lambda x: str(x).encode("ascii")

    def serialize(self):
        command = b"#%b" % (
            self.__class__.__name__
            + getattr(self, "append", "")
            + getattr(self, "x", "")
        ).encode("ascii")
        arguments = [
            self._serializers.get(self.__fields__[k].type_, self._default_serializer)(v)
            for k, v in self.dict().items()
        ]
        return (b" ".join((command, *arguments))) + b"\n"


class GET_DATA(Request):
    pass


class GET_UNBUFFERED_DATA(Request):
    pass


class GET_DATA_AND_LEVELS(Request):
    pass


class GET_UNBUFFERED_DATA_AND_LEVELS(Request):
    pass


class GET_SPECTRUM(Request):
    pass


class HELP(Request):
    pass


class IDN(Request):
    append = "?"


class GET_CAPABILITIES(Request):
    pass


class GET_SN(Request):
    pass


class SAVE_SETTINGS(Request):
    pass


class REBOOT(Request):
    pass


class SET_IP_ADDRESS(Request):
    address: IPv4Address


class GET_IP_ADDRESS(Request):
    pass


class SET_IP_NETMASK(Request):
    mask: IPv4Address


class GET_IP_NETMASK(Request):
    pass


class SET_DEFAULT_GATEWAY(Request):
    gateway: IPv4Address


class GET_DEFAULT_GATEWAY(Request):
    pass


class SET_DHCP(Request):
    val: bool


class GET_DHCP(Request):
    pass


class RESTART_NETWORK(Request):
    pass


class SET_DNS_SERVER(Request):
    server: IPv4Address


class GET_DNS_SERVER(Request):
    pass


class WHO(Request):
    append = "?"


class WHOAMI(Request):
    append = "?"


class SET_DATE(Request):
    date: datetime


class SET_ENABLE_NTP(Request):
    val: bool


class GET_ENABLE_NTP(Request):
    pass


class SET_NTP_SERVER(Request):
    x: NTPServer
    server: IPv4Address


class GET_NTP_SERVERX(Request):
    x: NTPServer


class GET_CH_GAIN_DB(Request):
    ch: Channel


class SET_CH_GAIN_DB(Request):
    ch: Channel
    gain: float


class GET_NUM_DUT_CHANNELS(Request):
    pass


class SET_CH_NOISE_THRESH(Request):
    ch: Channel
    val: int


class GET_CH_NOISE_THRESH(Request):
    ch: Channel


class SET_AMP_CH(Request):
    ch: Channel


class GET_AMP_CH(Request):
    pass


class SET_MUX_LEVEL(Request):
    val: MultiplexerLevel


class GET_MUX_LEVEL(Request):
    pass


class SET_INDEX_OF_REFRACTION(Request):
    ch: Union[Channel, SubChannel]
    val: float


class GET_INDEX_OF_REFRACTION(Request):
    ch: Union[Channel, SubChannel]


class SET_USE_REFERENCES(Request):
    val: bool


class GET_USE_REFERENCES(Request):
    pass


class SET_REFERENCE(Request):
    ch: Union[Channel, SubChannel]
    sensor: int
    ref_wvl: float


class GET_REFERENCE(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


class CLEAR_REFERENCE(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


class SET_DATA_RATE_DIVIDER(Request):
    div: int


class GET_DATA_RATE_DIVIDER(Request):
    pass


class SET_DATA_INTERLEAVE(Request):
    interleave: int


class GET_DATA_INTERLEAVE(Request):
    pass


class SET_NUM_AVERAGES(Request):
    ch: Union[Channel, SubChannel]
    sensor: int
    avgs: int


class GET_NUM_AVERAGES(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


class SET_STREAMING_DATA(Request):
    val: bool


class GET_STREAMING_DATA(Request):
    pass


class SET_BUFFER_ENABLE(Request):
    val: bool


class GET_BUFFER_ENABLE(Request):
    pass


class GET_BUFFER_COUNT(Request):
    pass


class FLUSH_BUFFER(Request):
    pass


class SET_OPERATING_MODE(Request):
    mode: OperatingMode


class GET_OPERATING_MODE(Request):
    pass


class SET_TRIG_MODE(Request):
    mode: TrigMode


class GET_TRIG_MODE(Request):
    pass


class SET_TRIG_START_EDGE(Request):
    val: bool


class GET_TRIG_START_EDGE(Request):
    pass


class SET_TRIG_STOP_TYPE(Request):
    val: bool


class GET_TRIG_STOP_TYPE(Request):
    pass


class SET_TRIG_STOP_EDGE(Request):
    val: bool


class GET_TRIG_STOP_EDGE(Request):
    pass


class SET_TRIG_NUM_ACQ(Request):
    val: bool


class GET_TRIG_NUM_ACQ(Request):
    pass


class SET_AUTO_RETRIG(Request):
    val: bool


class GET_AUTO_RETRIG(Request):
    pass


class SW_TRIG_START(Request):
    pass


class SW_TRIG_STOP(Request):
    pass


class MEASURE_LOCATIONS(Request):
    pass


class APPLY_MEASURED_LOCATIONS(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


class GET_MEASURED_LOCATION(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


class SET_LOC_MEAS_CH_OFFSET_METERS(Request):
    ch: Union[Channel, SubChannel]
    val: int


class SET_SENSOR_LOCATION(Request):
    ch: Union[Channel, SubChannel]
    sensor: int
    val: int


class GET_SENSOR_LOCATION(Request):
    ch: Union[Channel, SubChannel]
    sensor: int


# Responses
class Response(BaseModel):
    def __init__(self, response: bytes):
        try:
            super().__init__(**self.parse(response))
        except:
            raise ValueError("Could not parse response")


class DATA(Response):
    granularity: int
    channel_1_peaks: List[int]
    channel_2_peaks: List[int]
    channel_3_peaks: List[int]
    channel_4_peaks: List[int]

    def parse(self, response: bytes):
        status_header = response[:STATUS_HEADER_LENGTH]
        granularity = unpack("<L", status_header[72:76])[0]
        cumulative_num_peaks = list(accumulate(unpack("<HHHH", status_header[16:24])))
        peaks = unpack(
            "<" + ("L" * cumulative_num_peaks[3]),
            response[
                STATUS_HEADER_LENGTH : STATUS_HEADER_LENGTH
                + (4 * cumulative_num_peaks[3])
            ],
        )
        channel_1_peaks = peaks[0 : cumulative_num_peaks[0]]
        channel_2_peaks = peaks[cumulative_num_peaks[0] : cumulative_num_peaks[1]]
        channel_3_peaks = peaks[cumulative_num_peaks[1] : cumulative_num_peaks[2]]
        channel_4_peaks = peaks[cumulative_num_peaks[2] : cumulative_num_peaks[3]]

        return {
            "granularity": granularity,
            "channel_1_peaks": channel_1_peaks,
            "channel_2_peaks": channel_2_peaks,
            "channel_3_peaks": channel_3_peaks,
            "channel_4_peaks": channel_4_peaks,
        }

