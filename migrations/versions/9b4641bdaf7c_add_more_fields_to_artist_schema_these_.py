"""Add more fields to artist schema

These new fields are all nullable

Revision ID: 9b4641bdaf7c
Revises: c7fc80add82d
Create Date: 2022-05-23 15:41:29.891309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4641bdaf7c'
down_revision = 'c7fc80add82d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('address', sa.String(length=120), nullable=False))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=False))
    op.add_column('Artist', sa.Column('seeking_decription', sa.String(length=120), nullable=False))
    op.add_column('Artist', sa.Column('seeking_talent', sa.Boolean(), nullable=False))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=False))
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'seeking_talent')
    op.drop_column('Artist', 'seeking_decription')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'address')
    # ### end Alembic commands ###
