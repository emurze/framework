from typing import NoReturn

from server.exceptions import HttpParserError
from server.ports import IParser
from server.utils import dec


class HTTPParser(IParser):
    def __init__(self):
        self.request = {}

    @staticmethod
    def _format_headers(headers) -> list | NoReturn:
        formatted_headers = []
        for header in headers:
            try:
                if header != b"":
                    key, val = header.split(b":", maxsplit=1)
                    val = val.strip()
                    formatted_headers.append((dec(key), dec(val)))
            except ValueError as ve:
                print(f"Error parsing header: {ve}")
        return formatted_headers

    def parse_request(self, data_http: bytes) -> dict | NoReturn:
        try:
            print(data_http)
            request, headers_body = data_http.split(b"\r\n", 1)
            method, path, type_version = request.split(b" ")
            *headers, body = headers_body.split(b"\r\n")
            http_type, http_version = type_version.split(b"/")

            self.request["method"] = dec(method)
            self.request["path"] = dec(path)
            self.request["type"] = dec(http_type).lower()
            self.request["http_version"] = dec(http_version)
            self.request["headers"] = self._format_headers(headers)
            self.request["body"] = dec(body)

        except (ValueError, IndexError) as e:
            print(f"Error parsing HTTP request: {e}")
            raise HttpParserError("Error parsing HTTP request")

        return self.request

    def serialize_http_response(self, responses: list[dict]) -> bytes:
        http_response = b""
        headers = {}

        for response in responses:
            response_type = response.get("type")

            # Todo: Rewrite it on Events if we extend
            if response_type == "http.response.start":
                status_code = response.get("status", 200)
                http_response += f"HTTP/1.1 {status_code} OK\r\n".encode()

                for header in response.get("headers", []):
                    key, value = header
                    headers[key] = value

            elif response_type == "http.response.body":
                http_response += b"\r\n".join(
                    [
                        f"{key.decode()}: {value.decode()}".encode()
                        for key, value in headers.items()
                    ]
                )
                http_response += b"\r\n\r\n" + response.get("body", b"")

        return http_response
