import asyncio
from collections.abc import Iterator

from ports import IServer
from server import ConnectionHandler, Server


def get_server(loop=None) -> Iterator[IServer]:
    if loop is None:  # 1 test
        loop = asyncio.get_event_loop()
    conn_handler = ConnectionHandler(loop)
    server = Server(loop, conn_handler)
    yield server  # 2 test
