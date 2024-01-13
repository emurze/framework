import asyncio


async def test_client_route(testing_server, test_client) -> None:
    task2 = asyncio.Task(test_client.get('http://0.0.0.0:8000'))
    assert await task2 == "Hello, World!"
