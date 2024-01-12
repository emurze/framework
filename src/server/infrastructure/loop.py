from dataclasses import dataclass
from typing import Optional, Any, Self

from server.ports import IEventLoop


@dataclass
class EventLoopProxy(IEventLoop):
    loop: Optional[Any] = None
    conn: Optional[Any] = None

    def set_loop(self, loop: Any) -> Self:
        self.loop = loop
        return self

    def set_conn(self, conn: Any) -> Self:
        self.conn = conn
        return self

    def close_connection(self) -> None:
        self.conn.close()

    async def sock_accept(self, server_sock: Any) -> tuple:
        return await self.loop.sock_accept(server_sock)

    async def sock_recv(self, batch: int) -> bytes:
        return await self.loop.sock_recv(self.conn, batch)

    async def sock_sendall(self, response: bytes) -> None:
        return await self.loop.sock_sendall(self.conn, response)
