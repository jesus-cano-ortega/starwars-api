"""empty message

Revision ID: f4b771d8f2d6
Revises: 27e53fd3ac4c
Create Date: 2022-03-01 22:01:24.798133

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f4b771d8f2d6'
down_revision = '27e53fd3ac4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character', 'affiliations')
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=False))
    op.create_unique_constraint(None, 'user', ['email'])
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'email')
    op.add_column('character', sa.Column('affiliations', mysql.VARCHAR(length=30), nullable=True))
    # ### end Alembic commands ###
