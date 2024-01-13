import aiohttp


class Client:
    @staticmethod
    async def get(url: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            content = await response.text()
        return content
