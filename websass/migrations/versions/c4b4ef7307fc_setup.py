"""setup

Revision ID: c4b4ef7307fc
Revises: 
Create Date: 2021-02-25 20:41:37.992889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4b4ef7307fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('tournament',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('organizer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organizer'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tournament_name'), 'tournament', ['name'], unique=False)
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('player_name', sa.String(length=64), nullable=True),
    sa.Column('is_bye', sa.Boolean(), nullable=True),
    sa.Column('recieved_bye', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_player_name'), 'player', ['player_name'], unique=True)
    op.create_table('round',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tournament', sa.Integer(), nullable=True),
    sa.Column('round_num', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tournament'], ['tournament.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('round', sa.Integer(), nullable=True),
    sa.Column('corp_player', sa.Integer(), nullable=True),
    sa.Column('runner_player', sa.Integer(), nullable=True),
    sa.Column('corp_score', sa.Integer(), nullable=True),
    sa.Column('runner_score', sa.Integer(), nullable=True),
    sa.Column('elim_game', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['corp_player'], ['player.id'], ),
    sa.ForeignKeyConstraint(['round'], ['round.id'], ),
    sa.ForeignKeyConstraint(['runner_player'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('match')
    op.drop_table('round')
    op.drop_index(op.f('ix_player_player_name'), table_name='player')
    op.drop_table('player')
    op.drop_index(op.f('ix_tournament_name'), table_name='tournament')
    op.drop_table('tournament')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###