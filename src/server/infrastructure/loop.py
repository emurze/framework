from asyncio import AbstractEventLoop
from socket import socket
from typing import Self, Any

from server.ports import IEventLoop


class EventLoop(IEventLoop):
    loop: AbstractEventLoop
    conn: socket

    def get_loop(self) -> int | Any:
        if hasattr(self, 'loop'):
            return self.loop
        else:
            return 0

    def set_loop(self, loop: Any) -> Self:
        self.loop = loop
        return self

    def set_conn(self, conn: socket) -> Self:
        self.conn = conn
        return self

    def close_connection(self) -> None:
        self.conn.close()

    async def sock_accept(self, server_sock: socket) -> tuple:
        return await self.loop.sock_accept(server_sock)

    async def sock_recv(self, batch: int) -> bytes:
        return await self.loop.sock_recv(self.conn, batch)

    async def sock_sendall(self, response: bytes) -> None:
        await self.loop.sock_sendall(self.conn, response)
