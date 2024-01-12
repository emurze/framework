import aiohttp

from tests.utils.ports import ITestClient


class Client(ITestClient):
    async def get(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            content = await response.text()

        return content


