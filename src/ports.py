import abc
from typing import Protocol, Any


class IConnectionHandler(Protocol):
    loop: Any

    @abc.abstractmethod
    async def handle(self, conn, batch: int = 0) -> None: ...


class IServer(Protocol):
    loop: Any
    connection_handler: IConnectionHandler
    server_sock: Any
    host: str
    port: int

    @abc.abstractmethod
    async def listen_for_connections(self) -> None: ...

    @abc.abstractmethod
    async def run(self, ) -> None: ...


class IParser(Protocol):
    pass
