import socket
import re
from struct import pack, unpack
from time import sleep


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
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.peak_streaming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peak_streaming_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.streaming = False

    def __enter__(self):
        self.command_socket.bind(("127.0.0.1", 51971))
        self.peak_streaming_socket.bind(("127.0.0.1", 51972))
        return self

    def __exit__(self, exception_type, value, traceback):
        self.command_socket.close()
        self.peak_streaming_socket.close()

    def start(self):
        self.command_socket.listen()
        conn, _ = self.command_socket.accept()
        conn.settimeout(1)
        while True:
            data = conn.recv(8)
            command_size = unpack("<H", data[2:4])
            arguments_size = unpack("<I", data[4:8])
            command = (conn.recv(command_size)).decode("ascii")
            _ = conn.recv(arguments_size)

            print("Command received:", command)
            response = self.respond(command)
            print("Replying with:", response)
            conn.sendall(response)

    def peak_streaming(self):
        self.peak_streaming_socket.listen()
        conn, _ = self.peak_streaming_socket.accept()
        conn.settimeout(1)
        while True:
            if self.streaming:
                conn.sendall(self.respond("#GetPeaks"))
                sleep(1)

    def respond(self, command):
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
            message = b"Laser scan speed set to 10 Hz."
            content = b""

        elif command == "#GetInstrumentUtcDateTime":
            message = b"The instrument date/time has been set to '2017-01-01 00:00:00'."
            content = pack("<HHHHHH", 2017, 1, 1, 0, 0, 0)

        elif command == "#GetNtpEnabled":
            message = b"NTP server is currently enabled."
            content = pack("<I", 1)

        message_size = pack("<H", len(message))
        content_size = pack("<I", len(content))
        response = status + option + message_size + content_size + message + content

        return response
