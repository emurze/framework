import pytest

from server.container import get_parser, get_server_socket, get_spec
from server.ports import IParser, ISocket, ISpec


@pytest.fixture
def parser() -> IParser:
    return get_parser()


@pytest.fixture
def socket() -> ISocket:
    return get_server_socket()


@pytest.fixture
def spec() -> ISpec:
    return get_spec()


@pytest.fixture
def valid_request(parser: IParser) -> dict:
    request = b"GET / HTTP/1.1\r\nHost: LERKA"
    return parser.parse_request(request)


@pytest.fixture
def filled_spec(spec: ISpec, valid_request: dict) -> ISpec:
    spec.setup(valid_request)
    return spec
