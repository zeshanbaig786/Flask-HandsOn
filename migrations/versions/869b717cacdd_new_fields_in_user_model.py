"""new fields in user model

Revision ID: 869b717cacdd
Revises: 847dbb6c6a68
Create Date: 2022-11-12 21:02:23.510057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '869b717cacdd'
down_revision = '847dbb6c6a68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postlikedby')

    op.create_table('PostLikedBy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('postId', sa.Integer(), nullable=False),
    sa.Column('likedOn', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    op.create_table('postlikedby',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('userId', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('postId', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('likedOn', mysql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('PostLikedBy')
    # ### end Alembic commands ###