import asyncio
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

from server.infrastructure.parser import HTTPParser
from server.ports import IParser, IConnectionHandler, IServer
from server.services.conn_handler import ConnectionHandler
from server.services.server import Server
from server.utils import get_app_from_str


def get_parser() -> IParser:
    return HTTPParser()


def get_conn_handler(parser: IParser = get_parser()) -> IConnectionHandler:
    return ConnectionHandler(parser)


def get_server(
    app: Callable,
    loop: Any,
    conn_handler: IConnectionHandler = get_conn_handler(),
    port: Optional[int] = None,
    host: Optional[str] = None,
) -> IServer:
    """
    Server Factory that injects dependencies
    """

    optional_kwargs = {}

    if port is not None:
        optional_kwargs["port"] = port

    if host is not None:
        optional_kwargs["host"] = host

    return Server(app, loop, conn_handler, **optional_kwargs)


@dataclass(frozen=True)
class ServerContainer:
    port: Optional[int] = None
    host: Optional[str] = None
    app: Callable = get_app_from_str(sys.argv)
    conn_handler: IConnectionHandler = field(default_factory=get_conn_handler)

    def run(self):
        loop = asyncio.get_event_loop()
        server = get_server(
            app=self.app,
            loop=loop,
            conn_handler=self.conn_handler,
            port=self.port,
            host=self.host,
        )
        loop.run_until_complete(server.run())
        loop.close()
