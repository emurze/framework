import asyncio
from dataclasses import dataclass

from server.ports import IServer, IConnectionHandler, IEventLoop, ISocket


@dataclass
class Server(IServer):
    loop: IEventLoop
    conn_handler: IConnectionHandler
    server_sock: ISocket

    async def listen_for_connections(self) -> None:
        """
        Waiting event that creates a new connection event delegating connection
        handling to connection handler
        """

        self.server_sock.listen()
        print(f"Listening on {self.server_sock.host}:{self.server_sock.port}")

        while True:
            conn, address = await self.loop.sock_accept(self.server_sock)
            print(f"Connection from {address[0]}")
            asyncio.Task(self.conn_handler.handle(self.loop.set_conn(conn)))

    def stop(self) -> None:
        """
        Closing server_sock will close the server
        """

        self.server_sock.close()

    async def run(self) -> None:
        """
        It's listen_for_connections() delegator.
        It can be extended for before and after operations.
        """

        await self.listen_for_connections()
