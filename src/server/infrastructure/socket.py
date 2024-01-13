from io import TextIOWrapper
import socket
from typing import NoReturn, Optional, Any

from server.ports import ISocket


class Socket(ISocket):
    _closed: bool = False
    host: str
    port: int
    socket: socket.socket

    def setup(
        self,
        *_,
        conn: Optional[Any] = None,
        host: str = "0.0.0.0",
        port: int = 8000
    ) -> None:
        if conn:
            self.socket = conn
        else:
            self.host = host
            self.port = port
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setblocking(False)
            self.socket.bind((host, port))

    def __repr__(self) -> str:
        return f'Socket({repr(self.socket)})'

    def __getstate__(self) -> NoReturn:
        raise TypeError(f"cannot pickle {self.__class__.__name__!r} object")

    def listen(self, *args, **kwargs):
        return self.socket.listen(*args, **kwargs)

    def dup(self):
        return self.socket.dup()

    def accept(self) -> tuple:
        conn, address = self.socket.accept()
        new_socket = Socket()
        new_socket.setup(conn=conn)
        return new_socket, address

    def recv(self, batch: int = 1024) -> bytes:
        return self.socket.recv(batch)

    def send(self, data: bytes) -> int:
        return self.socket.send(data)

    def setblocking(self, value: bool) -> None:
        self.socket.setblocking(value)

    def makefile(self, *args, **kwargs) -> TextIOWrapper:
        return self.socket.makefile(*args, **kwargs)

    def sendfile(self, file, offset=0, count=None):
        return self.socket.sendfile(file, offset, count)

    def close(self) -> None:
        self.socket.close()

    def detach(self) -> int:
        return self.socket.detach()

    @property
    def family(self):
        return self.socket.family

    @property
    def type(self):
        return self.socket.type

    def fileno(self) -> int:
        return self.socket.fileno()
