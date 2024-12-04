"""create a relation between permission and user tables

Revision ID: 6d4f02f84a0f
Revises: b44e5b004e80
Create Date: 2024-12-03 15:39:42.344400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d4f02f84a0f'
down_revision: Union[str, None] = 'b44e5b004e80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('permission_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'users', 'permissions', ['permission_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'permission_id')
    # ### end Alembic commands ###
