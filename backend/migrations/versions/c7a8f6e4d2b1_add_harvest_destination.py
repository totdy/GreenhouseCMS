"""add harvest destination

Revision ID: c7a8f6e4d2b1
Revises: 95da640e5993
Create Date: 2026-08-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7a8f6e4d2b1"
down_revision: Union[str, Sequence[str], None] = "95da640e5993"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add destination and backfill existing harvests."""
    op.add_column(
        "harvests",
        sa.Column("destination", sa.String(), nullable=True),
    )
    op.execute(
        sa.text("UPDATE harvests SET destination = 'Other' WHERE destination IS NULL")
    )

    with op.batch_alter_table("harvests") as batch_op:
        batch_op.alter_column(
            "destination",
            existing_type=sa.String(),
            nullable=False,
        )


def downgrade() -> None:
    """Remove destination from harvests."""
    with op.batch_alter_table("harvests") as batch_op:
        batch_op.drop_column("destination")
