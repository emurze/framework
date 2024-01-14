import asyncio
import sys
from asyncio import AbstractEventLoop
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Optional

from server.infrastructure.loop import EventLoop
from server.infrastructure.parser import HTTPParser
from server.infrastructure.socket import Socket
from server.infrastructure.spec import ASGISpec
from server.ports import (
    IParser,
    IConnectionHandler,
    IServer,
    ISpec,
    IEventLoop,
    ISocket,
)
from server.services.conn_handler import ConnectionHandler
from server.services.server import Server
from server.utils import get_app_from_str


def get_server_socket() -> ISocket:
    return Socket()


def get_event_loop() -> IEventLoop:
    return EventLoop()


def get_parser() -> IParser:
    return HTTPParser()


def get_spec() -> ISpec:
    return ASGISpec()


def get_conn_handler(
    parser: IParser = get_parser(),
    spec: ISpec = get_spec(),
    app: Optional[Callable] = None,
) -> IConnectionHandler:
    return ConnectionHandler(app, parser, spec)


def get_server(
    loop: Any,
    conn_handler: IConnectionHandler = get_conn_handler(),
    server_sock: ISocket = get_server_socket(),
    port: Optional[int] = None,
    host: Optional[str] = None,
) -> IServer:
    opt_kwargs: dict = {}

    if port is not None:
        opt_kwargs["port"] = port

    if host is not None:
        opt_kwargs["host"] = host

    server_sock.setup(**opt_kwargs)
    return Server(loop, conn_handler, server_sock)


@dataclass
class ServerContainer:
    app_factory: Callable = partial(get_app_from_str, sys.argv)
    port: Optional[int] = None
    host: Optional[str] = None
    event_loop: IEventLoop = field(default_factory=get_event_loop)
    server_sock: ISocket = field(default_factory=get_server_socket)
    conn_handler: IConnectionHandler = field(default_factory=get_conn_handler)

    _server: Optional[IServer] = field(init=False, default=None)
    _loop: Optional[AbstractEventLoop] = field(init=False, default=None)

    @property
    def loop(self):
        if self._loop is not None:
            return self._loop

    def stop(self) -> None:
        if self._server is not None:
            self._server.stop()

    def setup(self) -> None:
        self._loop = asyncio.new_event_loop()
        self.conn_handler.app = self.app_factory()  # app parsing process

    def run(self):
        self._server = get_server(
            loop=self.event_loop.set_loop(self._loop),
            conn_handler=self.conn_handler,
            server_sock=self.server_sock,
            port=self.port,
            host=self.host,
        )
        try:
            self._loop.run_until_complete(self._server.run())
        except KeyboardInterrupt:
            print("\nServer was stopped")
