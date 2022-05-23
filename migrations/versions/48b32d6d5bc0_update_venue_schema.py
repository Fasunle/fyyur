"""Update Venue schema

Revision ID: 48b32d6d5bc0
Revises: a24e9aad0362
Create Date: 2022-05-23 23:01:38.667254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48b32d6d5bc0'
down_revision = 'a24e9aad0362'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('address', sa.String(
                        length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=False),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=False),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.Column('genres', sa.String(length=120), nullable=False),
                    sa.Column('website_link', sa.String(
                        length=120), nullable=False),
                    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
                    sa.Column('seeking_description', sa.String(
                        length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('Venue')
