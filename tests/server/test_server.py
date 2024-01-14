import time

from server.container import (
    ServerContainer,
    get_event_loop,
    get_server_socket,
    get_conn_handler,
)


def test_container_init() -> None:
    ServerContainer(
        app_factory=lambda: 0,
        port=0,
        host="",
        event_loop=get_event_loop(),
        server_sock=get_server_socket(),
        conn_handler=get_conn_handler(),
    )


def test_server(server_container, test_client) -> None:
    response = test_client.get(host="0.0.0.0", path="/users/1")
    assert response.decode() == """\r\n\r\n[{"id":1,"username":"Vlad"}]"""
