"""user models update 3

Revision ID: 255adeaee61f
Revises: 
Create Date: 2022-06-05 19:15:30.357952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255adeaee61f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('areas',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('area', sa.String(length=200), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('state', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.Column('is_administrative_center', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('area')
    )
    op.create_table('commercial',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=1000), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('img', sa.String(length=100), nullable=False),
    sa.Column('owner', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('valid_to_date', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('premium_tiers',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tier', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tier')
    )
    op.create_table('redis_channels',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('redis_channel', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('redis_channel')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=1000), nullable=False),
    sa.Column('is_staff', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('date_joined', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('customers',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('conversation_reference', sa.LargeBinary(length=10000), nullable=False),
    sa.Column('member_id', sa.BigInteger(), nullable=False),
    sa.Column('lang', sa.Integer(), nullable=False),
    sa.Column('post_header', sa.LargeBinary(length=10000), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('passcode', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('premium_tier_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['premium_tier_id'], ['premium_tiers.id'], name='fk_customers_premium_tiers_id_premium_tier_id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('member_id'),
    sa.UniqueConstraint('nickname'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_customers_lang'), 'customers', ['lang'], unique=False)
    op.create_table('adv_goals',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('goals_1', sa.Integer(), nullable=False),
    sa.Column('goals_2', sa.Integer(), nullable=False),
    sa.Column('goals_3', sa.Integer(), nullable=False),
    sa.Column('goals_4', sa.Integer(), nullable=False),
    sa.Column('goals_5', sa.Integer(), nullable=False),
    sa.Column('goals_6', sa.Integer(), nullable=False),
    sa.Column('goals_7', sa.Integer(), nullable=False),
    sa.Column('goals_8', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('adv_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['adv_id'], ['customers.id'], name='fk_adv_goals_customers_id_adv_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('advertisements',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('who_for_whom', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('prefer_age', sa.Integer(), nullable=False),
    sa.Column('has_place', sa.Integer(), nullable=False),
    sa.Column('dating_time', sa.Integer(), nullable=False),
    sa.Column('dating_day', sa.Integer(), nullable=False),
    sa.Column('adv_text', sa.Text(), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=False),
    sa.Column('phone_is_hidden', sa.Boolean(), nullable=False),
    sa.Column('money_support', sa.Boolean(), nullable=False),
    sa.Column('redis_channel_main', sa.String(length=100), nullable=False),
    sa.Column('redis_channel_second', sa.String(length=100), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('valid_to_date', sa.DateTime(), nullable=False),
    sa.Column('area_id', sa.BigInteger(), nullable=True),
    sa.Column('large_city_near_id', sa.BigInteger(), nullable=True),
    sa.Column('publisher_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['areas.id'], name='fk_advertisements_areas_id_area_id'),
    sa.ForeignKeyConstraint(['large_city_near_id'], ['areas.id'], name='fk_advertisements_areas_id_large_city_near_id'),
    sa.ForeignKeyConstraint(['publisher_id'], ['customers.id'], name='fk_advertisements_customers_id_publisher_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_advertisements_age'), 'advertisements', ['age'], unique=False)
    op.create_index(op.f('ix_advertisements_prefer_age'), 'advertisements', ['prefer_age'], unique=False)
    op.create_index(op.f('ix_advertisements_redis_channel_main'), 'advertisements', ['redis_channel_main'], unique=False)
    op.create_index(op.f('ix_advertisements_redis_channel_second'), 'advertisements', ['redis_channel_second'], unique=False)
    op.create_index(op.f('ix_advertisements_who_for_whom'), 'advertisements', ['who_for_whom'], unique=False)
    op.create_table('blacklists',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('banned_member_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('customer_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='fk_blacklists_customers_id_customer_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blacklists_banned_member_id'), 'blacklists', ['banned_member_id'], unique=False)
    op.create_table('user_media_files',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('member_id', sa.BigInteger(), nullable=False),
    sa.Column('file', sa.String(length=100), nullable=False),
    sa.Column('file_type', sa.Integer(), nullable=False),
    sa.Column('privacy_type', sa.Integer(), nullable=False),
    sa.Column('file_temp_url', sa.String(length=200), nullable=False),
    sa.Column('is_archived', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('customer_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name='fk_user_media_files_customers_id_customer_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_media_files_member_id'), 'user_media_files', ['member_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_media_files_member_id'), table_name='user_media_files')
    op.drop_table('user_media_files')
    op.drop_index(op.f('ix_blacklists_banned_member_id'), table_name='blacklists')
    op.drop_table('blacklists')
    op.drop_index(op.f('ix_advertisements_who_for_whom'), table_name='advertisements')
    op.drop_index(op.f('ix_advertisements_redis_channel_second'), table_name='advertisements')
    op.drop_index(op.f('ix_advertisements_redis_channel_main'), table_name='advertisements')
    op.drop_index(op.f('ix_advertisements_prefer_age'), table_name='advertisements')
    op.drop_index(op.f('ix_advertisements_age'), table_name='advertisements')
    op.drop_table('advertisements')
    op.drop_table('adv_goals')
    op.drop_index(op.f('ix_customers_lang'), table_name='customers')
    op.drop_table('customers')
    op.drop_table('users')
    op.drop_table('redis_channels')
    op.drop_table('premium_tiers')
    op.drop_table('commercial')
    op.drop_table('areas')
    # ### end Alembic commands ###
