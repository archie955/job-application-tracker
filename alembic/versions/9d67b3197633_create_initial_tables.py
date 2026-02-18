"""create initial tables

Revision ID: 9d67b3197633
Revises: 
Create Date: 2026-02-18 13:39:21.708457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d67b3197633'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # users table
    application_status = sa.Enum(
        "NOT_APPLIED", "APPLIED", "INTERVIEW", "REJECTED", "SUCCESSFUL",
        name="application_status"
    )
    application_status.create(op.get_bind())

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("hashed_refresh_token", sa.Text(), nullable=True)
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"])

    # jobs table
    op.create_table(
        "jobs",

    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
