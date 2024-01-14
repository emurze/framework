import pytest

from server.exceptions import HttpParserError
from server.infrastructure.parser import HTTPParser


@pytest.mark.parametrize(
    "headers, result",
    (
        ([b"host: LERKA"], [("host", "LERKA")]),
        ([b"host: LERKA", b""], [("host", "LERKA")]),
    ),
)
def test_format_headers(
    parser: HTTPParser,
    headers: list[bytes],
    result: list,
) -> None:
    formatted_headers = parser._format_headers(headers)
    assert formatted_headers == result


def test_format_headers_errors(parser: HTTPParser) -> None:
    headers = [b"InvalidHeader"]
    with pytest.raises(HttpParserError):
        parser._format_headers(headers)


def test_parse_request(parser: HTTPParser) -> None:
    request = b"GET / HTTP/1.1\r\nHost: LERKA"
    parsed_request = parser.parse_request(request)
    assert parsed_request == {
        "body": "Host: LERKA",
        "headers": [],
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "type": "http",
    }


def test_parse_request_errors(parser: HTTPParser) -> None:
    request = b"GET / / HTTP/1.1\r\nHost: LERKA"
    with pytest.raises(HttpParserError):
        parser.parse_request(request)


def test_serialize_http_response(parser: HTTPParser) -> None:
    responses = [
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        },
        {
            "type": "http.response.body",
            "body": b"Hello World!",
        },
    ]
    http_response = parser.serialize_http_response(responses)
    assert (
        http_response
        == b"HTTP/1.1 200 OK\r\ncontent-type: text/plain\r\n\r\nHello World!"
    )
