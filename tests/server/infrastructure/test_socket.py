import socket as sock
from server.infrastructure.socket import Socket


def test_setup_default_args(socket: Socket) -> None:
    socket.setup()
    assert isinstance(socket.socket, sock.socket)


def test_setup_host_port(socket: Socket) -> None:
    socket.setup(host="0.0.0.0", port=8000)
    assert isinstance(socket.socket, sock.socket)


def test_setup_conn(socket: Socket) -> None:
    socket.setup(conn=sock.socket())
    assert isinstance(socket.socket, sock.socket)
