from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from contextlib import contextmanager, asynccontextmanager


async def get_async_session(engine: AsyncEngine):
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)

    return async_session_maker
