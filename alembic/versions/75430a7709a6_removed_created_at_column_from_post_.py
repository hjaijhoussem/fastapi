"""removed created_at column from post table

Revision ID: 75430a7709a6
Revises: 020c44d76eed
Create Date: 2025-03-12 14:10:45.227754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75430a7709a6'
down_revision: Union[str, None] = '020c44d76eed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('posts', 'created_at')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass
