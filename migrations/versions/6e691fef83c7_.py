"""empty message

Revision ID: 6e691fef83c7
Revises: 0e26945b7464
Create Date: 2022-08-30 22:18:36.882376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e691fef83c7'
down_revision = '0e26945b7464'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    # ### end Alembic commands ###