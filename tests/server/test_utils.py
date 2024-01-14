from unittest.mock import patch, MagicMock

import pytest

from server.exceptions import NoAppFound, AppParseError
from server.utils import dec, get_app_from_str


def test_dec() -> None:
    string = b"Hello"
    assert dec(string) == "Hello"


def test_get_app_from_str_errors() -> None:
    sys_args = ["___application_stop_it___"]
    with pytest.raises(SystemExit):
        with pytest.raises(AppParseError, match="not found"):
            get_app_from_str(sys_args)


def test_get_app_from_str_module_not_found() -> None:
    sys_args = ["1", "***var1:var2"]
    with pytest.raises(SystemExit):
        with pytest.raises(NoAppFound):
            get_app_from_str(sys_args)


@patch('server.utils.importlib.import_module')
def test_get_app_from_str_uses_import(mock_import_module: MagicMock()):
    mock_import_module.side_effect = ImportError("Some other error")
    sys_argv = ["", 'mock_module:mock_app']
    with pytest.raises(ImportError):
        get_app_from_str(sys_argv)
