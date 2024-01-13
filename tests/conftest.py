import threading
from typing import Any

import pytest
from aiohttp import web

from server.container import get_event_loop
from server.app_fixture import app_fixture
from server.container import ServerContainer
from server.ports import IEventLoop
from tests.base.client import Client


async def init_app() -> web.Application:
    async def handle(request):   # noqa: F841
        return web.Response(text="Hello, World!")

    app = web.Application()
    app.router.add_get('/', handle)
    return app


@pytest.fixture
async def testing_server(aiohttp_server: Any):
    app = await init_app()
    return await aiohttp_server(app, host="0.0.0.0", port=8000)


@pytest.fixture
def test_client():
    return Client()


@pytest.fixture
def loop() -> Any:
    return get_event_loop()


@pytest.fixture
def server(loop: IEventLoop) -> ServerContainer:
    server = ServerContainer(app_factory=lambda: app_fixture)
    thread = threading.Thread(target=server.run)
    thread.start()

    yield server

    thread.join()
