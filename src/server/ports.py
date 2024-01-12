from collections.abc import Callable
from typing import Protocol, Any


class IConnectionHandler(Protocol):
    spec: "ISpec"
    parser: "IParser"

    async def handle(self, loop: Any, conn: Any, batch: int = 0) -> None:
        ...


class IServer(Protocol):
    app: Callable
    loop: Any
    conn_handler: IConnectionHandler

    async def listen_for_connections(self) -> None:
        ...

    async def run(self) -> None:
        ...


class IParser(Protocol):
    def parse_request(self, data_http: bytes) -> dict:
        ...

    def serialize_http_response(self, responses: list[dict]) -> bytes:
        ...


class ISpec(Protocol):
    async def run(self, app: Callable) -> None:
        ...

    async def send(self, message: str) -> None:
        ...

    async def receive(self, message: str) -> None:
        ...
