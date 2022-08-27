"""empty message

Revision ID: 5f4da0b53539
Revises: 63f92b2b8b40
Create Date: 2022-08-27 13:49:34.540942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f4da0b53539'
down_revision = '63f92b2b8b40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('looking_artist', sa.Boolean(), nullable=False))
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('artist', 'looking_artist')
    # ### end Alembic commands ###
