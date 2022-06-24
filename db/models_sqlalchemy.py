# coding: utf-8
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text,
    Date,
    Numeric
)


from sqlalchemy.orm import relationship
from .engine import BASE

Base = BASE
metadata = Base.metadata


class Area(Base):
    __tablename__ = 'areas'

    id = Column(BigInteger, primary_key=True)
    area = Column(String(200), nullable=False, unique=True)
    city = Column(String(30), nullable=False)
    state = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)
    is_administrative_center = Column(Boolean, nullable=False)


class PremiumTier(Base):
    __tablename__ = 'premium_tiers'

    id = Column(BigInteger, primary_key=True)
    tier = Column(Integer, unique=True)


class RedisChannel(Base):
    __tablename__ = 'redis_channels'

    id = Column(BigInteger, primary_key=True)
    redis_channel = Column(String(200), nullable=False, unique=True)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger, primary_key=True)
    nickname = Column(String(50), nullable=False, unique=True)
    phone = Column(BigInteger, unique=True)
    email = Column(String(100), unique=True)
    conversation_reference = Column(LargeBinary)
    member_id = Column(BigInteger, unique=True)
    lang = Column(Integer)
    post_header = Column(LargeBinary)
    is_active = Column(Boolean, nullable=False)
    passcode = Column(String(50))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    premium_tier_id = Column(ForeignKey('premium_tiers.id', deferrable=True, initially='DEFERRED'), index=True)

    premium_tier = relationship('PremiumTier')


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(BigInteger, primary_key=True)
    who_for_whom = Column(Integer)
    age = Column(Integer, index=True)
    prefer_age = Column(Integer, index=True)
    has_place = Column(Integer, nullable=False)
    dating_time = Column(Integer, nullable=False)
    dating_day = Column(Integer, nullable=False)
    adv_text = Column(Text, nullable=False)
    location = Column(String(50))
    phone_is_hidden = Column(Boolean, nullable=False)
    money_support = Column(Boolean, nullable=False)
    redis_channel_main = Column(String(100), index=True)
    redis_channel_second = Column(String(100), index=True)
    is_published = Column(Boolean, nullable=False)
    created_at = Column(DateTime(True), nullable=False)
    area_id = Column(ForeignKey('areas.id', deferrable=True, initially='DEFERRED'), index=True)
    large_city_near_id = Column(ForeignKey('areas.id', deferrable=True, initially='DEFERRED'), index=True)
    publisher_id = Column(ForeignKey('customers.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    area = relationship('Area', primaryjoin='Advertisement.area_id == Area.id')
    large_city_near = relationship('Area', primaryjoin='Advertisement.large_city_near_id == Area.id')
    publisher = relationship('Customer')


class Blacklist(Base):
    __tablename__ = 'blacklists'

    id = Column(BigInteger, primary_key=True)
    banned_member_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(True), nullable=False)
    customer_id = Column(ForeignKey('customers.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    customer = relationship('Customer')


class UserMediaFile(Base):
    __tablename__ = 'user_media_files'

    id = Column(BigInteger, primary_key=True)
    member_id = Column(BigInteger)
    file = Column(String(100), nullable=False)
    file_type = Column(Integer)
    privacy_type = Column(Integer)
    file_temp_url = Column(String(200))
    is_archived = Column(Boolean, nullable=False)
    created_at = Column(DateTime(True), nullable=False)
    customer_id = Column(ForeignKey('customers.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    customer = relationship('Customer')


class AdvGoal(Base):
    __tablename__ = 'adv_goals'

    id = Column(BigInteger, primary_key=True)
    goals_1 = Column(Integer)
    goals_2 = Column(Integer)
    goals_3 = Column(Integer)
    goals_4 = Column(Integer)
    goals_5 = Column(Integer)
    goals_6 = Column(Integer)
    goals_7 = Column(Integer)
    goals_8 = Column(Integer)
    created_at = Column(DateTime(True), nullable=False)
    adv_id = Column(ForeignKey('advertisements.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    adv = relationship('Advertisement')
