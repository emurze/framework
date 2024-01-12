from dataclasses import dataclass
from typing import Any

from server.ports import IParser, IConnectionHandler


@dataclass
class ConnectionHandler(IConnectionHandler):
    parser: IParser

    async def handle(self, loop: Any, conn: Any, batch: int = 1024) -> None:
        try:
            data = await loop.sock_recv(conn, batch)
            request = self.parser.parse_request(data)

            # spec = self.spec.setup(request)
            #
            # asyncio.Task(spec.run(self.app))
            #
            # await spec.response_event.wait()
            #
            http_response = self.parser.serialize_http_response()
            await loop.sock_sendall(conn, b"Hello")
        finally:
            conn.close()


def func():
    handler = ConnectionHandler(lambda x: x, Spec, False)
