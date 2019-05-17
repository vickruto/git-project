"""empty message

Revision ID: 105b6435def0
Revises: f292edbc5537
Create Date: 2019-05-15 17:10:08.404406

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '105b6435def0'
down_revision = 'f292edbc5537'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('firstname', sa.String(length=60), nullable=True))
    op.add_column('participants', sa.Column('lastname', sa.String(length=60), nullable=True))
    op.create_index(op.f('ix_participants_firstname'), 'participants', ['firstname'], unique=False)
    op.create_index(op.f('ix_participants_lastname'), 'participants', ['lastname'], unique=False)
    op.drop_index('ix_participants_first_name', table_name='participants')
    op.drop_index('ix_participants_last_name', table_name='participants')
    op.drop_column('participants', 'first_name')
    op.drop_column('participants', 'last_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('last_name', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('participants', sa.Column('first_name', mysql.VARCHAR(length=60), nullable=True))
    op.create_index('ix_participants_last_name', 'participants', ['last_name'], unique=False)
    op.create_index('ix_participants_first_name', 'participants', ['first_name'], unique=False)
    op.drop_index(op.f('ix_participants_lastname'), table_name='participants')
    op.drop_index(op.f('ix_participants_firstname'), table_name='participants')
    op.drop_column('participants', 'lastname')
    op.drop_column('participants', 'firstname')
    # ### end Alembic commands ###
