import asyncio
from dataclasses import dataclass
from typing import Callable

from server.ports import IParser, IConnectionHandler, ISpec, IEventLoop


@dataclass
class ConnectionHandler(IConnectionHandler):
    app: Callable
    parser: IParser
    spec: ISpec

    async def _receive_request(self, loop: IEventLoop, batch: int) -> dict:
        data = await loop.sock_recv(batch)
        request = self.parser.parse_request(data)
        return request

    async def _delegate_handling(self, request: dict, app: Callable) -> list:
        self.spec.setup(request)
        asyncio.Task(self.spec.run(app))
        await self.spec.response_event.wait()
        return self.spec.response

    async def _send_response(self, loop: IEventLoop, spec_resp: list) -> None:
        response = self.parser.serialize_http_response(spec_resp)
        await loop.sock_sendall(response)

    async def handle(self, loop: IEventLoop, batch: int = 1024) -> None:
        try:
            request = await self._receive_request(loop, batch)
            spec_response = await self._delegate_handling(request, self.app)
            await self._send_response(loop, spec_response)
        finally:
            loop.close_connection()
