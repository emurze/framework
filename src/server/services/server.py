import asyncio
import socket
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from server.ports import IServer, IConnectionHandler


@dataclass
class Server(IServer):
    app: Callable
    loop: Any
    conn_handler: IConnectionHandler
    host: str = "0.0.0.0"
    port: int = 8000

    def __post_init__(self) -> None:
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.bind((self.host, self.port))

    async def listen_for_connections(self) -> None:
        """
        Async waiting task to create connections

        event: new_connection
        """

        self.server_sock.listen()
        print(f"Listening on {self.host}:{self.port}")

        while True:
            conn, address = await self.loop.sock_accept(self.server_sock)
            print(f"Connection from {address[0]}")
            asyncio.Task(self.conn_handler.handle(self.loop, conn))

    async def run(self) -> None:
        await self.listen_for_connections()
