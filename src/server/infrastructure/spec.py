import asyncio
from collections.abc import Callable
from typing import Optional

from server.ports import ISpec


class ASGISpec(ISpec):
    scope: Optional[dict] = None
    response: Optional[list] = None
    resp_event: Optional[asyncio.Event] = None

    def setup(self, request: dict) -> None:
        self.scope = {
            "asgi": {
                "version": "3.0",
                "spec_version": "2.0",
            },
            "method": request["method"],
            "path": request["path"],
            "type": request["type"],
            "http_version": request["version"],
            "headers": request["headers"],
            "body": request["body"],
        }
        self.response: list = []
        self.resp_event = asyncio.Event()

    async def run(self, app: Callable) -> None:
        await app(self.scope, self.receive, self.send)

    async def send(self, message: str) -> None:
        pass

    async def receive(self, message: str) -> None:
        pass
