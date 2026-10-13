"""add unique index for scheduled viewings

Revision ID: b85732b10ee0
Revises: 40d806d150e6
Create Date: 2026-10-13 12:55:34.699896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b85732b10ee0'
down_revision: Union[str, Sequence[str], None] = '40d806d150e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_index(
        "uq_active_viewing_client_property_time",
        "viewings",
        ["client_id", "property_id", "scheduled_at"],
        unique=True,
        postgresql_where=sa.text("status = 'scheduled'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_active_viewing_client_property_time",
        table_name="viewings",
    )

    # ### end Alembic commands ###
