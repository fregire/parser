import uuid

from src.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
import datetime


class Hub(BaseModel):
    __tablename__ = 'hub'

    hub: Mapped[str] = mapped_column(primary_key=True)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(Hub)

        return list(await session.scalars(query))
