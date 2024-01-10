import asyncio
from collections.abc import Iterator
from unittest.mock import Mock

import pytest

from factories import get_server
from src.ports import IServer


@pytest.fixture
def server(event_loop) -> IServer:
    return next(get_server(event_loop))
