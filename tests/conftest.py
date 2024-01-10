from collections.abc import Iterator

import pytest

from factories import get_server
from src.ports import IServer


@pytest.fixture
def server_gen() -> Iterator[IServer]:
    return get_server()
