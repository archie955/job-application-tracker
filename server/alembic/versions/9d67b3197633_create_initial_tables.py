"""create initial tables

Revision ID: 9d67b3197633
Revises: 
Create Date: 2026-02-18 13:39:21.708457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from server.models.models import application_status, assessment_type

# revision identifiers, used by Alembic.
revision: str = '9d67b3197633'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users table

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
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("employer", sa.String(length=200), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", application_status, nullable=False, default="NOT_APPLIED"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("user_id", "employer", "title")
    )
    op.create_index(op.f("ix_jobs_user_id"), "jobs", ["user_id"])

    # assessments table
    
    op.create_table(
        "assessments",
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("type", assessment_type, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, default=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"])
    )
    op.create_index(op.f("ix_assessments_job_id"), "assessments", ["job_id"])
    


def downgrade() -> None:
    op.drop_table("assessments")
    op.drop_table("jobs")
    op.drop_table("users")

