"""empty message

Revision ID: aebf0fa9d972
Revises: dda6bac5242c
Create Date: 2024-03-22 03:16:56.435085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aebf0fa9d972'
down_revision = 'dda6bac5242c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_column('amount')

    # ### end Alembic commands ###
