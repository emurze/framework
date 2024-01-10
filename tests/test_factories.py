import asyncio
from unittest import skip

from factories import get_server


@skip
def test_run_server_from_get_server_without_loop_arg() -> None:
    """
    Integration because of client
    """

    server = next(get_server())


@skip
def test_run_server_from_get_server_with_loop_arg() -> None:
    """
    Integration because of client
    """

    server = next(get_server(loop=asyncio.get_event_loop()))

