"""empty message

Revision ID: f6c5b5735383
Revises: 
Create Date: 2022-08-22 14:53:06.091418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6c5b5735383'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('Seeking_Description', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('Looking_Venue', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'Looking_Venue')
    op.drop_column('venue', 'Seeking_Description')
    op.drop_column('venue', 'website_link')
    # ### end Alembic commands ###