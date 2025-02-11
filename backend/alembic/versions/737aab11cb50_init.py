"""init

Revision ID: 737aab11cb50
Revises: 
Create Date: 2024-08-25 17:02:35.521834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '737aab11cb50'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('providers',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('spots', sa.Integer(), nullable=False),
    sa.Column('max_spots', sa.Integer(), nullable=False),
    sa.Column('account', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__providers'))
    )
    op.create_index(op.f('ix__providers__token'), 'providers', ['token'], unique=False)
    op.create_table('spots',
    sa.Column('additional_info', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('account', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__spots'))
    )
    op.create_index(op.f('ix__spots__token'), 'spots', ['token'], unique=False)
    op.create_table('users',
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('data', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users'))
    )
    op.create_table('aliases',
    sa.Column('base', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['base'], ['spots.id'], name=op.f('fk__aliases__base__spots')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__aliases'))
    )
    op.create_index(op.f('ix__aliases__base'), 'aliases', ['base'], unique=False)
    op.create_index(op.f('ix__aliases__name'), 'aliases', ['name'], unique=False)
    op.create_table('channels',
    sa.Column('spot', sa.UUID(), nullable=True),
    sa.Column('provider', sa.UUID(), nullable=True),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('messages_raw', sa.String(), nullable=False),
    sa.Column('open', sa.BOOLEAN(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('closed_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('dispose_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['provider'], ['providers.id'], name=op.f('fk__channels__provider__providers')),
    sa.ForeignKeyConstraint(['spot'], ['spots.id'], name=op.f('fk__channels__spot__spots')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__channels'))
    )
    op.create_index(op.f('ix__channels__code'), 'channels', ['code'], unique=True)
    op.create_index(op.f('ix__channels__provider'), 'channels', ['provider'], unique=False)
    op.create_index(op.f('ix__channels__spot'), 'channels', ['spot'], unique=False)
    op.create_table('provider_spots',
    sa.Column('provider_id', sa.UUID(), nullable=False),
    sa.Column('spot_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk__provider_spots__provider_id__providers')),
    sa.ForeignKeyConstraint(['spot_id'], ['spots.id'], name=op.f('fk__provider_spots__spot_id__spots')),
    sa.PrimaryKeyConstraint('provider_id', 'spot_id', name=op.f('pk__provider_spots'))
    )
    op.create_table('subscriptions',
    sa.Column('spot_id', sa.UUID(), nullable=True),
    sa.Column('provider_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('expires_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk__subscriptions__provider_id__providers')),
    sa.ForeignKeyConstraint(['spot_id'], ['spots.id'], name=op.f('fk__subscriptions__spot_id__spots')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__subscriptions'))
    )
    op.create_index(op.f('ix__subscriptions__created_at'), 'subscriptions', ['created_at'], unique=False)
    op.create_index(op.f('ix__subscriptions__expires_at'), 'subscriptions', ['expires_at'], unique=False)
    op.create_index(op.f('ix__subscriptions__provider_id'), 'subscriptions', ['provider_id'], unique=False)
    op.create_index(op.f('ix__subscriptions__spot_id'), 'subscriptions', ['spot_id'], unique=False)
    op.create_table('spot_channels',
    sa.Column('spot_id', sa.UUID(), nullable=False),
    sa.Column('channel_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], name=op.f('fk__spot_channels__channel_id__channels')),
    sa.ForeignKeyConstraint(['spot_id'], ['spots.id'], name=op.f('fk__spot_channels__spot_id__spots')),
    sa.PrimaryKeyConstraint('spot_id', 'channel_id', name=op.f('pk__spot_channels'))
    )
    op.create_table('users_channels',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('channel_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], name=op.f('fk__users_channels__channel_id__channels')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__users_channels__user_id__users')),
    sa.PrimaryKeyConstraint('user_id', 'channel_id', name=op.f('pk__users_channels'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_channels')
    op.drop_table('spot_channels')
    op.drop_index(op.f('ix__subscriptions__spot_id'), table_name='subscriptions')
    op.drop_index(op.f('ix__subscriptions__provider_id'), table_name='subscriptions')
    op.drop_index(op.f('ix__subscriptions__expires_at'), table_name='subscriptions')
    op.drop_index(op.f('ix__subscriptions__created_at'), table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_table('provider_spots')
    op.drop_index(op.f('ix__channels__spot'), table_name='channels')
    op.drop_index(op.f('ix__channels__provider'), table_name='channels')
    op.drop_index(op.f('ix__channels__code'), table_name='channels')
    op.drop_table('channels')
    op.drop_index(op.f('ix__aliases__name'), table_name='aliases')
    op.drop_index(op.f('ix__aliases__base'), table_name='aliases')
    op.drop_table('aliases')
    op.drop_table('users')
    op.drop_index(op.f('ix__spots__token'), table_name='spots')
    op.drop_table('spots')
    op.drop_index(op.f('ix__providers__token'), table_name='providers')
    op.drop_table('providers')
    # ### end Alembic commands ###
