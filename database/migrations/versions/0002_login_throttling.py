"""Login throttling: failed sign-in records (ADR-012).

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-08 20:44:00.451055
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = '0002'
down_revision: str | None = '0001'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('login_attempts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('ip_address', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_login_attempts'))
    )
    op.create_index('ix_login_attempts_email_created', 'login_attempts', ['email', 'created_at'], unique=False)
    op.create_index('ix_login_attempts_ip_created', 'login_attempts', ['ip_address', 'created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_login_attempts_ip_created', table_name='login_attempts')
    op.drop_index('ix_login_attempts_email_created', table_name='login_attempts')
    op.drop_table('login_attempts')
