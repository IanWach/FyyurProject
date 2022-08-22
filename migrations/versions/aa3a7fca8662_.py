"""empty message

Revision ID: aa3a7fca8662
Revises: f6c5b5735383
Create Date: 2022-08-22 14:54:43.204138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa3a7fca8662'
down_revision = 'f6c5b5735383'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('Seeking_Description', sa.String(length=500), nullable=True))
    op.add_column('artist', sa.Column('Looking_Artist', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'Looking_Artist')
    op.drop_column('artist', 'Seeking_Description')
    op.drop_column('artist', 'website_link')
    # ### end Alembic commands ###
