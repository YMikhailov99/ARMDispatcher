"""Added required tables

Revision ID: e547596e20a3
Revises: a9bb797ccf4b
Create Date: 2022-03-14 23:57:56.912872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e547596e20a3'
down_revision = 'a9bb797ccf4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('objects_barriers_links', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('objects_barriers_links', 'id')
    # ### end Alembic commands ###