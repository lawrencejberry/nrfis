from datetime import datetime
from ipaddress import ip_address

import pytest

from ..x55.x55_protocol import (
    GetFirmwareVersion,
    GetInstrumentName,
    IsReady,
    GetDutChannelCount,
    GetPeaks,
    EnablePeakDataStreaming,
    DisablePeakDataStreaming,
    GetPeakDataStreamingStatus,
    GetPeakDataStreamingDivider,
    GetPeakDataStreamingAvailableBuffer,
    GetLaserScanSpeed,
    SetLaserScanSpeed,
    GetAvailableLaserScanSpeeds,
    SetInstrumentUtcDateTime,
    GetInstrumentUtcDateTime,
    GetNtpEnabled,
    SetNtpEnabled,
    SetNtpServer,
    GetNtpServer,
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
    NtpServer,
)

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("x55_instrument")]


async def test_get_firmware_version(x55_client):
    response = FirmwareVersion(await x55_client.command.execute(GetFirmwareVersion()))

    assert response.status == True
    assert response.message == "Firmware Version: 12.12.1.20099."
    assert response.content == "12.12.1.20099"


async def test_get_instrument_name(x55_client):
    response = InstrumentName(await x55_client.command.execute(GetInstrumentName()))

    assert response.status == True
    assert response.message == "The instrument name is Lab-1."
    assert response.content == "Lab-1"


async def test_is_ready(x55_client):
    response = Ready(await x55_client.command.execute(IsReady()))

    assert response.status == True
    assert response.message == "The System is ready."
    assert response.content == True


async def test_get_dut_channel_count(x55_client):
    response = DutChannelCount(await x55_client.command.execute(GetDutChannelCount()))

    assert response.status == True
    assert response.message == "The number of DUT channels is 16."
    assert response.content == 16


async def test_get_peaks(x55_client):
    response = Peaks(await x55_client.command.execute(GetPeaks()))

    assert response.status == True
    assert response.message == ""
    assert response.timestamp.timestamp() == 10.5
    assert response.content == [20 * [800.0] for i in range(16)]


async def test_enable_peak_data_streaming(x55_client):
    response = Response(await x55_client.command.execute(EnablePeakDataStreaming()))

    assert response.status == True
    assert response.message == "The data streaming socket has been enabled."
    assert response.content == b""


async def test_disable_peak_data_streaming(x55_client):
    response = Response(await x55_client.command.execute(DisablePeakDataStreaming()))

    assert response.status == True
    assert response.message == "The data streaming socket has been disabled."
    assert response.content == b""


async def test_get_peak_data_streaming_status(x55_client):
    response = PeakDataStreamingStatus(
        await x55_client.command.execute(GetPeakDataStreamingStatus())
    )

    assert response.status == True
    assert response.message == "The data streaming is currently disabled."
    assert response.content == False


async def test_get_peak_data_streaming_divider(x55_client):
    response = PeakDataStreamingDivider(
        await x55_client.command.execute(GetPeakDataStreamingDivider())
    )

    assert response.status == True
    assert response.message == "The data streaming divider is currently 1."
    assert response.content == 1


async def test_get_peak_data_streaming_available_buffer(x55_client):
    response = PeakDataStreamingAvailableBuffer(
        await x55_client.command.execute(GetPeakDataStreamingAvailableBuffer())
    )

    assert response.status == True
    assert response.message == "The available streaming data buffer is currently 100%."
    assert response.content == 100


async def test_get_laser_scan_speed(x55_client):
    response = LaserScanSpeed(await x55_client.command.execute(GetLaserScanSpeed()))

    assert response.status == True
    assert response.message == "The current scan speed is 10 Hz."
    assert response.content == 10


async def test_set_laser_scan_speed(x55_client):
    response = Response(await x55_client.command.execute(SetLaserScanSpeed(speed=100)))

    assert response.status == True
    assert response.message == "Laser scan speed set to 100 Hz."
    assert response.content == b""


async def test_get_available_laser_scan_speeds(x55_client):
    response = AvailableLaserScanSpeeds(
        await x55_client.command.execute(GetAvailableLaserScanSpeeds(speed=100))
    )

    assert response.status == True
    assert response.message == "The available scan speed are 2 10 in Hz."
    assert response.content == [2, 10]


async def test_set_instrument_utc_datetime(x55_client):
    response = Response(
        await x55_client.command.execute(
            SetInstrumentUtcDateTime(dt=datetime(2020, 1, 1))
        )
    )

    assert response.status == True
    assert (
        response.message
        == "The instrument date/time has been set to '2020-01-01 00:00:00'."
    )
    assert response.content == b""


async def test_get_instrument_utc_datetime(x55_client):
    response = InstrumentUtcDateTime(
        await x55_client.command.execute(GetInstrumentUtcDateTime())
    )

    assert response.status == True
    assert (
        response.message
        == "The instrument date/time has been set to '2017-01-01 00:00:00'."
    )
    assert response.content.timestamp() == 1483228800.0


async def test_get_ntp_enabled(x55_client):
    response = NtpEnabled(await x55_client.command.execute(GetNtpEnabled()))

    assert response.status == True
    assert response.message == "NTP server is currently enabled."
    assert response.content == True


async def test_set_ntp_enabled(x55_client):
    response = Response(await x55_client.command.execute(SetNtpEnabled(enabled=True)))

    assert response.status == True
    assert response.message == "The NTP Server has been enabled."
    assert response.content == b""


async def test_set_ntp_server(x55_client):
    response = Response(
        await x55_client.command.execute(
            SetNtpServer(address=ip_address("98.175.203.200"))
        )
    )

    assert response.status == True
    assert response.message == "The NTP Server has been set to '98.175.203.200'."
    assert response.content == b""


async def test_get_ntp_server(x55_client):
    response = NtpServer(await x55_client.command.execute(GetNtpServer()))

    assert response.status == True
    assert response.message == "NTP server is currently set to '98.175.203.200'."
    assert response.content == ip_address("98.175.203.200")


async def test_peaks_streaming(x55_client):
    count = 1
    async for response in x55_client.stream():
        assert response.status == True
        assert response.message == ""
        assert response.timestamp.timestamp() == 10.5
        assert response.content == [20 * [800.0] for i in range(16)]

        count += 1
        if count > 5:
            x55_client.streaming = False
