"""add user table

Revision ID: 19e60233e7b2
Revises: 805f16f15632
Create Date: 2024-11-17 16:43:38.485539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e60233e7b2'
down_revision: Union[str, None] = '805f16f15632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
                    #email unqiue constraint)
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
