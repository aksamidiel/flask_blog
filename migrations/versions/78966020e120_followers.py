"""followers

Revision ID: 78966020e120
Revises: c80a2db6574e
Create Date: 2020-06-10 15:54:41.884511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78966020e120'
down_revision = 'c80a2db6574e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
