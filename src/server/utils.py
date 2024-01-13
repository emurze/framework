import importlib
from typing import Callable, NoReturn

from server.exceptions import AppParseError, NoAppFound


def dec(obj: bytes) -> str:
    return obj.decode("utf-8")


def get_app_from_str(sys_argv: list) -> Callable | NoReturn:
    try:
        input_str = sys_argv[1]
        module_str, attribute_str = input_str.split(":")
    except (ValueError, IndexError):
        raise AppParseError('App path variable is not found')

    try:
        module = importlib.import_module(module_str)
        _app = getattr(module, attribute_str)
        return _app
    except ModuleNotFoundError as exc:
        raise NoAppFound from exc
