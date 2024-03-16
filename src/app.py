from src.hub_parser import  HubParser
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
import time
from src.models.article import Article
from src.schemas.article import GetArticleFilters


class App:
    def __init__(self, engine: AsyncEngine, hub: str, parse_timeout: int):
        self.engine = engine
        self.hub = hub
        self.parse_timeout = parse_timeout

    async def __process(self):
        session = async_sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self.engine
        )()
        articles = HubParser(self.hub).parse()
        for article in articles:
            try:
                if not await Article.get_article(filters=GetArticleFilters(link=article.link), session=session):
                    await Article.create_article(create_data=article, session=session)
                    await session.commit()
            finally:
                await session.close()

    async def start(self):
        while True:
            await self.__process()
            time.sleep(self.parse_timeout)

    async def stop(self):
        await self.engine.dispose()