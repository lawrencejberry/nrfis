import socket
import re
from time import sleep


class MockServer:
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
