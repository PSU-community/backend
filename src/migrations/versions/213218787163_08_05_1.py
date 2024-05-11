"""08_05.1

Revision ID: 213218787163
Revises: 40a43d5c5a1e
Create Date: 2024-05-08 20:03:28.523823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '213218787163'
down_revision: Union[str, None] = '40a43d5c5a1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subcategories_category_id_fkey', 'subcategories', type_='foreignkey')
    op.create_foreign_key(None, 'subcategories', 'categories', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subcategories', type_='foreignkey')
    op.create_foreign_key('subcategories_category_id_fkey', 'subcategories', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###
