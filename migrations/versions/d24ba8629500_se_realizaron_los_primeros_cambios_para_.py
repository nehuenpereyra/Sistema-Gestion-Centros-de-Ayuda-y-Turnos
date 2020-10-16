"""Se realizaron los primeros cambios para agregar roles y permisos de usuario

Revision ID: d24ba8629500
Revises: 1bb89b7157a7
Create Date: 2020-10-15 10:30:20.557150

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd24ba8629500'
down_revision = '1bb89b7157a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
