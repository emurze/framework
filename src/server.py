import asyncio
import socket
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Any

from ports import IServer, IConnectionHandler


# class HTTPParser(IParser):
#     pass


@dataclass
class ConnectionHandler(IConnectionHandler):
    # parser: IParser
    loop: AbstractEventLoop

    async def handle(self, conn: Any, batch: int = 1024) -> None:
        try:
            while request := await self.loop.sock_recv(conn, batch):  # client
                response = f"Hello {request.decode()}".encode()
                await self.loop.sock_sendall(conn, response)
        finally:
            conn.close()


class Server(IServer):
    def __init__(
        self,
        loop: AbstractEventLoop,
        conn_handler: IConnectionHandler,
        host: str = "0.0.0.0",
        port: int = 8000,
    ) -> None:
        # inject
        self.loop = loop
        self.conn_handler = conn_handler

        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allows the reusing of a local address that is still waiting
        # to time out after the socket is closed.
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Allows async execution
        self.server_sock.setblocking(False)

        self.server_sock.bind((host, port))

    async def listen_for_connections(self) -> None:
        self.server_sock.listen()
        print(f'Listening on {self.host}:{self.port}')

        while True:
            # 3 test several clients
            conn, address = await self.loop.sock_accept(self.server_sock)
            print(f'Connection from {address[0]}')
            asyncio.Task(self.conn_handler.handle(conn))

    async def run(self) -> None:
        await self.listen_for_connections()
