from io import TextIOWrapper
import socket
from typing import NoReturn, Optional, Any

from server.ports import IServerSocket


class ServerSocket(IServerSocket):
    _closed: bool = False
    host: Optional[str] = None
    port: Optional[int] = None
    socket: Optional[Any] = None

    def setup(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind((host, port))

    def __repr__(self) -> str:
        return repr(self.socket)

    def __getstate__(self) -> NoReturn:
        raise TypeError(f"cannot pickle {self.__class__.__name__!r} object")

    def listen(self, *args, **kwargs):
        return self.socket.listen(*args, **kwargs)

    def dup(self):
        return self.socket.dup()

    def accept(self) -> tuple:
        return self.socket.accept()

    def makefile(self, *args, **kwargs) -> TextIOWrapper:
        return self.socket.makefile(*args, **kwargs)

    def sendfile(self, file, offset=0, count=None):
        return self.socket.sendfile(file, offset, count)

    def close(self) -> None:
        return self.socket.close()

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
