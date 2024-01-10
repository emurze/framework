import asyncio
from collections.abc import Iterator

import pytest

from src.ports import IServer


def test_init(server_gen: Iterator[IServer]) -> None:
    server = next(server_gen)
    assert server.server_sock
    assert server.host
    assert server.port


@pytest.mark.asyncio
async def test_accept_connection(server_gen: Iterator[IServer]) -> None:
    server = next(server_gen)

    try:
        await asyncio.wait_for(server.run(), timeout=3)
    except TimeoutError:
        assert 0
