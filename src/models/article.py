import uuid

from src.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
import datetime

from src.schemas.article import BaseArticle, GetArticleFilters


class Article(BaseModel):
    __tablename__ = 'article'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    headline: Mapped[str]
    publish_date: Mapped[datetime.datetime]
    link: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    author_link: Mapped[str]
    content: Mapped[str]
    hub: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    @classmethod
    async def create_article(cls, create_data: BaseArticle, session: AsyncSession):
        article = cls().fill(**create_data.model_dump())

        session.add(article)

        return article

    @classmethod
    async def get_article(cls, filters: GetArticleFilters, session: AsyncSession):
        if not filters.model_dump():
            return
        query = select(cls)
        if filters.link:
            query = query.where(cls.link == filters.link)

        if not (result := await session.scalar(query)):
            return

        return result
