import asyncio
import sys
from asyncio import AbstractEventLoop
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

from server.infrastructure.loop import EventLoopProxy
from server.infrastructure.parser import HTTPParser
from server.infrastructure.sockets import ServerSocket
from server.infrastructure.spec import ASGISpec
from server.ports import (
    IParser, IConnectionHandler, IServer, ISpec, IEventLoop, IServerSocket
)
from server.services.conn_handler import ConnectionHandler
from server.services.server import Server
from server.utils import get_app_from_str


def get_server_socket() -> IServerSocket:
    return ServerSocket()


def get_event_loop() -> IEventLoop:
    return EventLoopProxy()


def get_parser() -> IParser:
    return HTTPParser()


def get_spec() -> ISpec:
    return ASGISpec()


def get_conn_handler(
    parser: IParser = get_parser(),
    spec: ISpec = get_spec(),
    app: Callable = get_app_from_str(sys.argv),
) -> IConnectionHandler:
    return ConnectionHandler(app, parser, spec)


def get_server(
    loop: Any,
    conn_handler: IConnectionHandler = get_conn_handler(),
    server_sock: IServerSocket = get_server_socket(),
    port: Optional[int] = None,
    host: Optional[str] = None,
) -> IServer:
    opt_kwargs = {}

    if port is not None:
        opt_kwargs["port"] = port

    if host is not None:
        opt_kwargs["host"] = host

    server_sock.setup(**opt_kwargs)
    return Server(loop, conn_handler, server_sock)


@dataclass(frozen=True)
class ServerContainer:
    port: Optional[int] = None
    host: Optional[str] = None
    event_loop: IEventLoop = field(default_factory=get_event_loop)
    server_sock: IServerSocket = field(default_factory=get_server_socket)
    conn_handler: IConnectionHandler = field(default_factory=get_conn_handler)

    def run(self):
        loop = asyncio.get_event_loop()
        server = get_server(
            loop=self.event_loop.set_loop(loop),
            conn_handler=self.conn_handler,
            server_sock=self.server_sock,
            port=self.port,
            host=self.host,
        )
        loop.run_until_complete(server.run())
        loop.close()
