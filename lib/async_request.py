import aiohttp
from typing import Union


async def get(string: str) -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(string) as resp:

            if resp.status == 404:
                return None

            return await resp.json(content_type=None)
