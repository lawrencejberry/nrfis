import socket
import re
from struct import pack, unpack
import asyncio


class Mockx30Instrument:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.streaming = False

    def __enter__(self):
        self.socket.bind(("127.0.0.1", 9500))
        return self

    def __exit__(self, exception_type, value, traceback):
        self.socket.close()

    def start(self):
        self.socket.listen()
        conn, _ = self.socket.accept()
        conn.settimeout(1)
        while True:
            while True:
                try:
                    data = conn.recv(1024)
                    if b"\n" in data:
                        break
                except socket.timeout:
                    if self.streaming:
                        data = b"#GET_DATA\n"
                        break

            command = re.search("#(.+?)\n", data.decode("ascii")).group(1)
            print("Command received:", command)
            response = self.respond(command)
            print("Replying with:", response)
            conn.sendall(response)

    def respond(self, command):
        if command == "GET_DATA":
            data = bytes(88)
            if self.streaming:
                data += b"XXXXXXXX"
            length = format(len(data), "010").encode("ascii")
            response = length + data
            return response

        elif command == "SET_STREAMING_DATA 1":
            self.streaming = True
            data = b"Streaming data enabled.\n"
            length = format(len(data), "010").encode("ascii")
            response = length + data
            return response

        elif command == "SET_STREAMING_DATA 0":
            self.streaming = False
            data = b"Streaming data disabled.\nZZZZZZZZ"
            length = format(len(data), "010").encode("ascii")
            response = length + data
            return response


class Mockx55Instrument:
    def __init__(self):
        self.command = None
        self.peaks = None
        self.streaming = False

    async def __aenter__(self):
        self.command = await asyncio.start_server(
            self.start_command, host="127.0.0.1", port=51971
        )
        self.peaks = await asyncio.start_server(
            self.start_peaks, host="127.0.0.1", port=51972
        )
        return self

    async def __aexit__(self, exception_type, value, traceback):
        self.command.close()
        self.peaks.close()

    async def start_command(self, reader, writer):
        while True:
            data = await reader.read(8)
            command_size = unpack("<H", data[2:4])[0]
            arguments_size = unpack("<I", data[4:8])[0]
            command = (await reader.read(command_size)).decode("ascii")
            arguments = await reader.read(arguments_size)

            if command == "#EnablePeakDataStreaming":
                self.streaming = True

            if command == "#DisablePeakDataStreaming":
                self.streaming = False

            response = self.respond(command, arguments)
            writer.write(response)

    async def start_peaks(self, _, writer):
        response = self.respond("#GetPeaks")
        while True:
            if self.streaming:
                writer.write(response)
            await asyncio.sleep(0.1)

    def respond(self, command, arguments=None):
        status = pack("<B", 0)
        option = pack("<B", 0)

        if command == "#GetFirmwareVersion":
            message = b"Firmware Version: 12.12.1.20099."
            content = b"12.12.1.20099"

        elif command == "#GetInstrumentName":
            message = b"The instrument name is Lab-1."
            content = b"Lab-1"

        elif command == "#IsReady":
            message = b"The System is ready."
            content = pack("<B", 1)

        elif command == "#GetDutChannelCount":
            message = b"The number of DUT channels is 16."
            content = pack("<I", 16)

        elif command == "#GetPeaks":
            message = b""

            header_length = pack("<H", 56)
            header_version = pack("<H", 0)
            pad = bytes(4)
            serial_number = bytes(8)
            timestamp_seconds = pack("<I", 10)
            timestamp_nanoseconds = pack("<I", 500000000)
            num_peaks = pack("<" + 16 * "H", *(16 * [20]))
            peaks = pack("<" + 320 * "d", *(320 * [800]))

            content = (
                header_length
                + header_version
                + pad
                + serial_number
                + timestamp_seconds
                + timestamp_nanoseconds
                + num_peaks
                + peaks
            )

        elif command == "#EnablePeakDataStreaming":
            message = b"The data streaming socket has been enabled."
            content = b""

        elif command == "#DisablePeakDataStreaming":
            message = b"The data streaming socket has been disabled."
            content = b""

        elif command == "#GetPeakDataStreamingStatus":
            if self.streaming:
                message = b"The data streaming is currently enabled."
                content = pack("<I", 1)
            else:
                message = b"The data streaming is currently disabled."
                content = pack("<I", 0)

        elif command == "#GetPeakDataStreamingDivider":
            message = b"The data streaming divider is currently 1."
            content = pack("<I", 1)

        elif command == "#GetPeakDataStreamingAvailableBuffer":
            message = b"The available streaming data buffer is currently 100%."
            content = pack("<I", 100)

        elif command == "#GetLaserScanSpeed":
            message = b"The current scan speed is 10 Hz."
            content = pack("<I", 10)

        elif command == "#SetLaserScanSpeed":
            message = b"Laser scan speed set to %b Hz." % arguments
            content = b""

        elif command == "#GetAvailableLaserScanSpeeds":
            message = b"The available scan speed are 2 10 in Hz."
            content = pack("<II", 2, 10)

        elif command == "#SetInstrumentUtcDateTime":
            message = b"The instrument date/time has been set to '2020-01-01 00:00:00'."
            content = b""

        elif command == "#GetInstrumentUtcDateTime":
            message = b"The instrument date/time has been set to '2017-01-01 00:00:00'."
            content = pack("<HHHHHH", 2017, 1, 1, 0, 0, 0)

        elif command == "#GetNtpEnabled":
            message = b"NTP server is currently enabled."
            content = pack("<I", 1)

        elif command == "#SetNtpEnabled":
            message = b"The NTP Server has been enabled."
            content = b""

        elif command == "#SetNtpServer":
            message = b"The NTP Server has been set to '98.175.203.200'."
            content = b""

        elif command == "#GetNtpServer":
            message = b"NTP server is currently set to '98.175.203.200'."
            content = b"98.175.203.200"

        message_size = pack("<H", len(message))
        content_size = pack("<I", len(content))
        response = status + option + message_size + content_size + message + content

        return response
