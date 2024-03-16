import datetime
import uuid

from pydantic import BaseModel


class BaseArticle(BaseModel):
    headline: str
    publish_date: datetime.datetime
    link: str
    author: str
    author_link: str
    content: str
    hub: str


class Article(BaseArticle):
    id: uuid.UUID


class GetArticleFilters(BaseModel):
    link: str
