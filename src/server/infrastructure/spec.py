import asyncio
from collections.abc import Callable
from typing import Optional

from server.ports import ISpec, Event


class ASGISpec(ISpec):
    scope: Optional[dict] = None
    response: Optional[list] = None
    response_event: Optional[Event] = None

    def setup(self, request: dict) -> None:
        self.scope = {
            "asgi": {
                "version": "3.0",
                "spec_version": "2.0",
            },
            "method": request["method"],
            "path": request["path"],
            "type": request["type"],
            "http_version": request["http_version"],
            "headers": request["headers"],
            "body": request["body"],
            "query_string": "",
        }
        self.response: list = []
        self.response_event = asyncio.Event()

    async def run(self, app: Callable) -> None:
        await app(self.scope, self.receive, self.send)

    async def send(self, message: dict) -> None:
        if message.get('type') == "http.response.body":
            self.response.append(message)
            self.response_event.set()

    async def receive(self, message: str) -> dict:
        message = {
            "type": "http.request",
            "body": self.scope.get("body"),
            "more_body": False,
        }
        return message
