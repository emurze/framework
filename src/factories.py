import asyncio
from collections.abc import Generator, Iterator

from ports import IServer
from server import ConnectionHandler, Server


def get_server() -> Iterator[IServer]:
    loop = asyncio.get_event_loop()
    conn_handler = ConnectionHandler(loop)
    server = Server(loop, conn_handler)
    yield server
