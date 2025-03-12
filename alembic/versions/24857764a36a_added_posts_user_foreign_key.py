"""added posts user foreign key

Revision ID: 24857764a36a
Revises: 0f8a85b187f8
Create Date: 2025-03-12 14:33:02.181533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24857764a36a'
down_revision: Union[str, None] = '0f8a85b187f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
