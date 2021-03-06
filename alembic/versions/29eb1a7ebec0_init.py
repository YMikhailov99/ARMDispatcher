"""init

Revision ID: 29eb1a7ebec0
Revises: 
Create Date: 2022-04-26 15:28:15.182331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29eb1a7ebec0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('barriers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('gsm_number_vp', sa.String(length=50), nullable=True),
    sa.Column('sip_number_vp', sa.String(length=50), nullable=True),
    sa.Column('camera_url', sa.String(), nullable=True),
    sa.Column('camdirect_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('objects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_and_address', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_free_departure_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_jkh_passage_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_delivery_passage_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_collection_passage_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_garbtrucks_passage_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_post_passage_prohibited', sa.Boolean(), nullable=False),
    sa.Column('is_free_taxi_passage_prohibited', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password_sha256', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('objects_barriers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('barrier_id', sa.String(), nullable=True),
    sa.Column('object_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['barrier_id'], ['barriers.id'], ),
    sa.ForeignKeyConstraint(['object_id'], ['objects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_actions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_actions')
    op.drop_table('objects_barriers')
    op.drop_table('users')
    op.drop_table('objects')
    op.drop_table('barriers')
    # ### end Alembic commands ###
