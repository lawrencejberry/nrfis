import socket


class MockServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __enter__(self):
        self.socket.bind(("127.0.0.1", 9500))
        return self

    def __exit__(self, exception_type, value, traceback):
        self.socket.close()

    def respond(self):
        while True:
            self.socket.listen()
            conn, _ = self.socket.accept()
            while True:
                data = conn.recv(1024)
                if b"\n" in data:
                    break
            print("Data received at server:", data)
            acknowledgment_response = b"0000000088"
            data_response = bytes(88)
            reply = acknowledgment_response + data_response
            print("Replying with:", reply)
            conn.sendall(reply)

    def stream(self):
        while True:
            self.socket.listen()
            conn, _ = self.socket.accept()
            while True:
                data = conn.recv(1024)
                if b"\n" in data:
                    break
            while True:
                acknowledgment_response = b"0000000096"
                data_response = bytes(88)
                message_end = b"XXXXXXXX"
                reply = acknowledgment_response + data_response + message_end
                conn.sendall(reply)
