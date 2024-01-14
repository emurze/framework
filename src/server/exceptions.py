class CLIError(Exception):
    def __init__(self, message: str = "", exit_code: int = 1) -> None:
        self._print(message)
        exit(exit_code)

    @staticmethod
    def _print(message: str) -> None:
        print(f"Error: {message}")


class BaseError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class NoAppFound(CLIError):
    pass


class AppParseError(CLIError):
    pass


class HttpParserError(BaseError):
    pass
