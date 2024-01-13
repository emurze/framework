import asyncio
import socket
from typing import Any

from server.container import ServerContainer
from server.ports import IEventLoop


def test_set_loop_self_return(loop: IEventLoop, event_loop):
    res = loop.set_loop(event_loop)
    assert res == loop


def test_set_loop(loop: IEventLoop, event_loop):
    loop.set_loop(event_loop)
    assert loop.loop == event_loop


def test_close_connection(loop: IEventLoop, testing_server: Any):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', 8000))
    loop.set_conn(sock)
    loop.close_connection()
    assert loop.conn._closed


async def test_sock_accept(loop: IEventLoop, server: ServerContainer):
    # await loop.sock_accept(server.server_sock)
    print(await asyncio.sleep(3, result='LERKA'))
