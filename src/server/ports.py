import abc
from collections.abc import Callable
from typing import Protocol, Any, Optional, Self


class IConnectionHandler(Protocol):
    """
    Handling connection is:
        - Awaiting and parsing a request
        - Delegating it to an appropriate application
        - serializing response from the application and send to a client
    """

    app: Callable
    spec: "ISpec"
    parser: "IParser"

    @abc.abstractmethod
    async def handle(self, loop: "IEventLoop", batch: int = 0) -> None:
        ...


class IServer(Protocol):
    """
    Responsible for:
        - Infinity waiting for client action
        - Creating connection events for each
    """

    app: Callable
    loop: "IEventLoop"
    conn_handler: IConnectionHandler

    @abc.abstractmethod
    async def listen_for_connections(self) -> None:
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        ...

    @abc.abstractmethod
    async def run(self) -> None:
        ...


class IParser(Protocol):
    """
    Responsible for:
        - Parsing request
        - DeSerializing ISpec events like:
            - "http.response.start"
            - "http.response.body"
    """

    @abc.abstractmethod
    def parse_request(self, data_http: bytes) -> dict:
        ...

    @abc.abstractmethod
    def serialize_http_response(self, responses: list[dict]) -> bytes:
        ...


class Event(Protocol):
    """
    Async lib feature
    """

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
    async def receive(self) -> dict:
        ...


class ISocket(Protocol):
    """
    It's Encapsulation of socket mechanism that provides:
        - server_sock creating
        - client_sock wrapper
        - storage for host, port
    """

    host: str
    port: int

    @abc.abstractmethod
    def setup(
        self,
        *,
        conn: Optional[Any] = None,
        host: str = "0.0.0.0",
        port: int = 8000
    ) -> None:
        ...

    @abc.abstractmethod
    def listen(self, conn_length: int = 0) -> None:
        ...

    @abc.abstractmethod
    def accept(self) -> tuple:
        ...

    @abc.abstractmethod
    def recv(self, batch: int = 0) -> bytes:
        ...

    @abc.abstractmethod
    def send(self, data: bytes) -> int:
        ...

    @abc.abstractmethod
    def close(self) -> None:
        ...

    @abc.abstractmethod
    def fileno(self) -> int:
        ...


class IEventLoop(Protocol):
    """
    Delegate ISocket execution in async way
    """

    loop: Any
    conn: Any

    @abc.abstractmethod
    def set_conn(self, conn: Any) -> Self:
        ...

    @abc.abstractmethod
    def get_loop(self) -> Any:
        ...

    @abc.abstractmethod
    def set_loop(self, loop: Any) -> Self:
        ...

    @abc.abstractmethod
    async def sock_accept(self, server_sock: Any) -> tuple:
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
