import socket

SERVER_PORT = 8081


class Client:
    def _make_response(self, request: str, batch: int = 1024) -> bytes:
        self.sock.send(request.encode())
        return self.sock.recv(batch)

    def _create_connection(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def get(self, host: str, path: str, port: int = SERVER_PORT) -> bytes:
        self._create_connection(host, port)
        request = f"GET {path} HTTP/1.1\r\nHost: example.com\r\n\r\n"
        return self._make_response(request)
