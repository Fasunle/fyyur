"""Set some more constraint for Artist Schema

Revision ID: a24e9aad0362
Revises: 
Create Date: 2022-05-23 22:49:17.803703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24e9aad0362'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=False),
                    sa.Column('genres', sa.String(length=120), nullable=False),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=False),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.Column('website_link', sa.String(
                        length=120), nullable=False),
                    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
                    sa.Column('seeking_description', sa.String(
                        length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('Artist')
