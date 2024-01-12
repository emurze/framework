import abc
from collections.abc import Callable
from typing import Protocol, Any, Optional, Self


class IConnectionHandler(Protocol):
    app: Callable
    spec: "ISpec"
    parser: "IParser"

    @abc.abstractmethod
    async def handle(self, loop: "IEventLoop", batch: int = 0) -> None:
        ...


class IServer(Protocol):
    app: Callable
    loop: Any
    conn_handler: IConnectionHandler

    @abc.abstractmethod
    async def listen_for_connections(self) -> None:
        ...

    @abc.abstractmethod
    async def run(self) -> None:
        ...


class IParser(Protocol):
    @abc.abstractmethod
    def parse_request(self, data_http: bytes) -> dict:
        ...

    @abc.abstractmethod
    def serialize_http_response(self, responses: list[dict]) -> bytes:
        ...


class Event(Protocol):
    @abc.abstractmethod
    def set(self):
        ...

    @abc.abstractmethod
    async def wait(self):
        ...


class ISpec(Protocol):
    scope: Optional[dict] = None
    response: Optional[list] = None
    response_event: Optional[Event] = None

    @abc.abstractmethod
    def setup(self, request: dict) -> None:
        ...

    @abc.abstractmethod
    async def run(self, app: Callable) -> None:
        ...

    @abc.abstractmethod
    async def send(self, message: dict) -> None:
        ...

    @abc.abstractmethod
    async def receive(self, message: str) -> dict:
        ...


class IEventLoop(Protocol):
    loop: Optional[Any]
    conn: Optional[Any]

    @abc.abstractmethod
    def set_conn(self, conn: Any) -> Self: ...

    @abc.abstractmethod
    def set_loop(self, loop: Any) -> Self: ...

    @abc.abstractmethod
    async def sock_accept(self, server_sock) -> tuple:
        ...

    @abc.abstractmethod
    async def sock_recv(self, batch: int) -> bytes:
        ...

    @abc.abstractmethod
    async def sock_sendall(self, response: bytes) -> None:
        ...

    @abc.abstractmethod
    def close_connection(self) -> None:
        ...


class IServerSocket(Protocol):
    host: str
    port: int

    def setup(self, host: str = "0.0.0.0", port: int = 8000) -> None: ...

    def listen(self, *args, **kwargs):  ...
