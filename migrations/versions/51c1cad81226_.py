"""empty message

Revision ID: 51c1cad81226
Revises: de6d57f30791
Create Date: 2024-03-22 02:51:11.578138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51c1cad81226'
down_revision = 'de6d57f30791'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Float(), nullable=False))
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('due',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.alter_column('due',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=False)
        batch_op.alter_column('type',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('amount')

    # ### end Alembic commands ###
