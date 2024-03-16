"""init

Revision ID: c3e7381c1ecf
Revises: 
Create Date: 2024-03-16 12:37:22.764111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func, ForeignKey
from sqlalchemy.types import DateTime, String, UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = 'c3e7381c1ecf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "article",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("headline", String, nullable=False),
        sa.Column("publish_date", DateTime, nullable=False),
        sa.Column("link", String, nullable=False, unique=True),
        sa.Column("author", String, nullable=False),
        sa.Column("author_link", String, nullable=False),
        sa.Column("content", String, nullable=False),
        sa.Column("hub", String, nullable=False),

        sa.Column("created_at", DateTime, server_default=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("article")
