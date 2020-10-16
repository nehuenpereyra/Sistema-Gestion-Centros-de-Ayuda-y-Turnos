"""Segunda prueba de migracion

Revision ID: 1bb89b7157a7
Revises: 5dfdd1781cf6
Create Date: 2020-10-13 19:32:22.896232

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1bb89b7157a7'
down_revision = '5dfdd1781cf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'otro_campo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('otro_campo', mysql.VARCHAR(length=30), nullable=True))
    # ### end Alembic commands ###
