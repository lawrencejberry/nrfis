import socket

HOST = "10.0.0.126"
PORT = 1852


class Synchronousx30Client:
    """Synchronous client to interact with Micron Optics x30 boxes."""

    ACKNOWLEDGEMENT_LENGTH = 10

    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.connect((self.host, self.port))

    def end(self):
        self.socket.close()

    def read(self, command: bytes):
        self.socket.sendall(command + b"\n")
        message_length = int(self.socket.recv(self.ACKNOWLEDGEMENT_LENGTH))
        message = self.socket.recv(message_length)
        status_header = message[:88]
        try:
            data = message[89:]
        except IndexError:
            data = None

        return status_header, data

    def get_data(self):
        return self.read(b"#GET_DATA")

    def get_unbuffered_data(self):
        return self.read(b"#GET_UNBUFFERED_DATA")

    def get_data_and_levels(self):
        return self.read(b"#GET_DATA_AND_LEVELS")

    def get_unbuffered_data_and_levels(self):
        return self.read(b"#GET_UNBUFFERED_DATA_AND_LEVELS")

    def get_spectrum(self):
        return self.read(b"#GET_SPECTRUM")

    def get_high_speed_fs(self):
        return self.read(b"#GET_HIGH_SPEED_FS")

    def help(self):
        return self.read(b"#HELP")

    def idn(self):
        return self.read(b"#IDN?")

    def get_capabilities(self):
        return self.read(b"#GET_CAPABILITIES")

    def get_sn(self):
        return self.read(b"#GET_SN")

    def save_settings(self):
        return self.read(b"#SAVE_SETTINGS")

    def reboot(self):
        return self.read(b"#REBOOT")
