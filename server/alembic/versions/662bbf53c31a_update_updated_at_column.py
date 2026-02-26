"""update updated_at column

Revision ID: 662bbf53c31a
Revises: 9d67b3197633
Create Date: 2026-02-23 19:16:51.741378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '662bbf53c31a'
down_revision: Union[str, Sequence[str], None] = '9d67b3197633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "jobs",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now()
    )
    pass


def downgrade() -> None:
    op.alter_column(
        "jobs",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onpudate=None
    )
    pass
