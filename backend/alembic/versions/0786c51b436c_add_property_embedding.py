
"""add property embedding

Revision ID: 0786c51b436c
Revises: b85732b10ee0
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# Alembic revision identifiers
revision: str = "0786c51b436c"
down_revision: Union[str, Sequence[str], None] = "b85732b10ee0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "properties",
        sa.Column(
            "embedding",
            Vector(1536),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("properties", "embedding")
