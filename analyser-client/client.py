import socket

from protocol import Request, GET_DATA, SET_STREAMING_DATA


class x30Client:
    """
    Client to interact with an sm130 fibre optic analyser box. Reflects the TCP protocol as far as possible.
    See the Micron Optics User Guide, Revision 1.139 section 4.4.4.5 for details.
    """

    ACKNOWLEDGEMENT_LENGTH = 10  # bytes
    STATUS_HEADER_LENGTH = 88  # bytes

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # State
        self.host = "10.0.0.126"
        self.port = 1852
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

    def connect(self):
        self.socket.connect((self.host, self.port))
        response = self.execute(GET_DATA())
        status_header = response[:88]
        self.update_status(status_header)

    def close(self):
        self.socket.close()

    def read(self, override_length: int = None) -> bytes:
        length = int(self.socket.recv(self.ACKNOWLEDGEMENT_LENGTH))
        if length is not None:  # Override message length if provided
            length = override_length
        response = self.socket.recv(length)
        return response

    def execute(self, request: Request, override_length: int = None) -> bytes:
        self.socket.sendall(request.serialize())
        return self.read(override_length)

    def update_status(self, status_header: bytes):
        self.fs_radix = int(status_header[0:8], 2)
        self.fw_version = status_header[16:24].decode("ascii")
        self.secondary_fan = bool(status_header[27] == b"1")
        self.primary_fan = bool(status_header[28] == b"1")
        self.calibration_fault = bool(status_header[30] == b"1")
        self.switch_position = int(status_header[48:50], 2)
        self.mux_level = int(status_header[49:51], 2)
        self.triggering_mode = int(status_header[52:54], 2)
        self.operating_mode = int(status_header[54:56], 2)
        self.num_peaks_detected = status_header[128:192]
        self.error = status_header[376:384].decode("ascii")
        self.buffer = status_header[384:392].decode("ascii")
        self.header_version = status_header[392:400].decode("ascii")
        self.granularity = int(status_header[576:608], 2)
        self.full_spectrum_start_wvl = int(status_header[640:672], 2)
        self.full_spectrum_end_wvl = int(status_header[672:], 2)

    def stream_data(self):
        self.streaming = bool(int(self.execute(SET_STREAMING_DATA(val=True))))
        while self.streaming:
            response = self.read()
            # Then process the response
        self.execute(SET_STREAMING_DATA(val=False))
