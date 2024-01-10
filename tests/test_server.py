import asyncio
import socket
from unittest import skip
from unittest.mock import patch, Mock
import aiohttp

import pytest
from pytest_mock import MockFixture

from src.ports import IServer


@pytest.mark.parametrize(
    "attr",
    (
        'server_sock',
        'host',
        'port',
    )
)
def test_init(server: IServer, attr: str) -> None:
    assert getattr(server, attr)


@skip
async def test_server_one_client_success(server: IServer) -> None:
    """
    Integration test for listen_for_connections() and ConnectionHandler()
    :param server:
    :return:
    """


@skip
async def test_server_two_clients_success(server: IServer) -> None:
    """
    Integration test for listen_for_connections() and ConnectionHandler()
    :param server:
    :return:
    """


async def test_run(server: IServer, mocker: MockFixture) -> None:
    listen_called = False

    async def mock_listen():
        nonlocal listen_called
        listen_called = True

    mocker.patch.object(server, 'listen_for_connections',
                        side_effect=mock_listen)
    await server.run()

    assert listen_called
