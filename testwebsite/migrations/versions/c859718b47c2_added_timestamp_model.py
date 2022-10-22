"""added Timestamp model

Revision ID: c859718b47c2
Revises: 
Create Date: 2022-10-22 11:23:45.832418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c859718b47c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_stamps',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('timestamp')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_stamps')
    # ### end Alembic commands ###