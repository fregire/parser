import asyncio

from src.hub_parser import  HubParser
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
import time
from src.models import Article, Hub
from src.schemas.article import GetArticleFilters
from src.utils import get_async_session


class App:
    def __init__(self, engine: AsyncEngine, parse_timeout: int):
        self.engine = engine
        self.parse_timeout = parse_timeout
        self.wait_hubs_timeout = 5

    async def start(self):
        while True:
            print("Getting hubs...")
            has_hubs = await self.__process()
            if not has_hubs:
                print("Cant find any hubs to process")
                await asyncio.sleep(self.wait_hubs_timeout)
            else:
                print("Waiting for next parsing")
                await asyncio.sleep(self.parse_timeout)

    async def __process(self) -> bool:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False, autoflush=False, autocommit=False)

        async with async_session() as session:
            hubs = await Hub.get_all(session=session)

        if not hubs:
            return False

        for hub in hubs:
            async with async_session() as session:
                await self.__process_hub(hub=hub.hub, session=session)

        return True

    async def __process_hub(self, hub: str, session: AsyncSession):
        articles = await HubParser(hub).parse()
        for article in articles:
            try:
                if not await Article.get_article(filters=GetArticleFilters(link=article.link), session=session):
                    await Article.create_article(create_data=article, session=session)
                    await session.commit()
            finally:
                await session.close()

    async def stop(self):
        await self.engine.dispose()
