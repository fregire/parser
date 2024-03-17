from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
import aiohttp


async def get_async_session(engine: AsyncEngine):
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)

    return async_session_maker


async def get_page(url) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
