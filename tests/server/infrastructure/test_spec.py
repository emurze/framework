from typing import Any
from unittest.mock import AsyncMock, call

from server.infrastructure.spec import ASGISpec
from server.ports import ISpec


def test_setup(filled_spec: ISpec) -> None:
    assert filled_spec.scope
    assert filled_spec.response == []
    assert filled_spec.response_event


async def test_run_app(filled_spec: ISpec) -> None:
    app = AsyncMock()
    await filled_spec.run(app)
    assert app.await_args == call(
        filled_spec.scope, filled_spec.receive, filled_spec.send
    )


async def test_send(filled_spec: ISpec) -> None:
    message = {"type": "http.response.body"}
    await filled_spec.send(message)
    assert filled_spec.response == [message]
    assert filled_spec.response_event.is_set()


async def test_send_do_nothing(filled_spec: ISpec) -> None:
    message: dict[str, Any] = {}
    await filled_spec.send(message)
    assert filled_spec.response == []
    assert not filled_spec.response_event.is_set()


async def test_receive_event(filled_spec: ASGISpec) -> None:
    res = await filled_spec.receive()
    assert isinstance(res, dict)
    assert res.get("type")
