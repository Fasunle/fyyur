"""Show model is a child table of Artist and Venue

This model has two foreign keys

Revision ID: 917f9b5ec861
Revises: 48b32d6d5bc0
Create Date: 2022-05-23 23:26:02.381749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917f9b5ec861'
down_revision = '48b32d6d5bc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Show',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('Show')
