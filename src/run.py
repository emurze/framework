import asyncio
from collections.abc import Iterator

from factories import get_server
from ports import IServer


async def main(server_gen: Iterator[IServer]) -> None:
    server = next(server_gen)
    await server.run()


if __name__ == '__main__':
    new_server = get_server()
    asyncio.run(main(new_server))
