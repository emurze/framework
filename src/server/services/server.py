import asyncio
from dataclasses import dataclass

from server.ports import IServer, IConnectionHandler, IEventLoop, IServerSocket


@dataclass
class Server(IServer):
    loop: IEventLoop
    conn_handler: IConnectionHandler
    server_sock: IServerSocket

    async def listen_for_connections(self) -> None:
        """
        Async waiting task to create connection using connection handler
        """

        self.server_sock.listen()
        print(f"Listening on {self.server_sock.host}:{self.server_sock.port}")

        while True:
            conn, address = await self.loop.sock_accept(self.server_sock)
            print(f"Connection from {address[0]}")
            asyncio.Task(self.conn_handler.handle(self.loop.set_conn(conn)))

    async def run(self) -> None:
        await self.listen_for_connections()
