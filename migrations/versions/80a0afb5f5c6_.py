"""empty message

Revision ID: 80a0afb5f5c6
Revises: a9b1c53119b0
Create Date: 2024-03-21 21:35:43.813261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a0afb5f5c6'
down_revision = 'a9b1c53119b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Coach',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('month', sa.String(length=100), nullable=False),
    sa.Column('urgency', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('due', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('month'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Hall',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month', sa.String(length=100), nullable=False),
    sa.Column('urgency', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('due', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('month')
    )
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_column('amount')

    op.drop_table('Hall')
    op.drop_table('Coach')
    # ### end Alembic commands ###
