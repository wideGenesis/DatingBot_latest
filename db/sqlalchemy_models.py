# # coding: utf-8
# from typing import Optional
#
# from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text, text
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# metadata = Base.metadata
#
# # TODO! server_default=text("nextval('areas_id_seq'::regclass)") UNcommented if parse tables from another ORM,
# #  else SqlAlchemy create tables comment this lines. Driver SYNC = export DB_DRIVER=postgresql
#
#
# class Area(Base):
#     __tablename__ = 'areas'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('areas_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     area = Column(String(200), nullable=False, unique=True)
#     city = Column(String(50), nullable=False)
#     state = Column(String(50), nullable=False)
#     country = Column(String(50), nullable=False)
#     is_administrative_center = Column(Boolean, nullable=False)
#
#
# class Commercial(Base):
#     __tablename__ = 'commercial'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('commercial_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     title = Column(String(1000), nullable=False)
#     description = Column(String(1000), nullable=False)
#     img = Column(String(100), nullable=False)
#     owner = Column(String(100), nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=False)
#     valid_to_date = Column(DateTime, nullable=False)
#     is_active = Column(Boolean, nullable=False)
#
#
# class PremiumTier(Base):
#     __tablename__ = 'premium_tiers'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('premium_tiers_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     tier = Column(String(200), nullable=False, unique=True)
#
#
# class RedisChannel(Base):
#     __tablename__ = 'redis_channels'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('redis_channels_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     redis_channel = Column(String(500), nullable=False, unique=True)
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     email = Column(String(50), nullable=False, unique=True)
#     username = Column(String(50), nullable=False, unique=True)
#     password_hash = Column(String(1000), nullable=False)
#
#
# class Customer(Base):
#     __tablename__ = 'customers'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('customers_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     nickname = Column(String(50), nullable=False, unique=True)
#     phone = Column(BigInteger, nullable=False, unique=True)
#     email: Optional[str] = Column(String(100), nullable=True, unique=True)
#     conversation_reference = Column(LargeBinary, nullable=False)
#     member_id = Column(BigInteger, nullable=False, unique=True)
#     lang = Column(Integer, nullable=False, index=True)
#     post_header: Optional[bytes] = Column(LargeBinary, nullable=True)
#     is_active = Column(Boolean, nullable=False)
#     passcode: Optional[str] = Column(String(50), nullable=True)
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=False)
#     premium_tier_id = Column(ForeignKey('premium_tiers.id'))
#
#     premium_tier = relationship('PremiumTier')
#
#
# class AdvGoal(Base):
#     __tablename__ = 'adv_goals'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('adv_goals_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     goals_1 = Column(Integer, nullable=False)
#     goals_2 = Column(Integer, nullable=False)
#     goals_3 = Column(Integer, nullable=False)
#     goals_4 = Column(Integer, nullable=False)
#     goals_5 = Column(Integer, nullable=False)
#     goals_6 = Column(Integer, nullable=False)
#     goals_7 = Column(Integer, nullable=False)
#     goals_8 = Column(Integer, nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     adv_id = Column(ForeignKey('customers.id'))
#
#     adv = relationship('Customer')
#
#
# class Advertisement(Base):
#     __tablename__ = 'advertisements'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('advertisements_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     who_for_whom = Column(Integer, nullable=False, index=True)
#     age = Column(Integer, nullable=False, index=True)
#     prefer_age = Column(Integer, nullable=False, index=True)
#     has_place = Column(Integer, nullable=False)
#     dating_time = Column(Integer, nullable=False)
#     dating_day = Column(Integer, nullable=False)
#     adv_text = Column(Text, nullable=False)
#     location = Column(String(50), nullable=False)
#     phone_is_hidden = Column(Boolean, nullable=False)
#     money_support = Column(Boolean, nullable=False)
#     redis_channel_main = Column(String(100), nullable=False, index=True)
#     redis_channel_second = Column(String(100), nullable=False, index=True)
#     is_published = Column(Boolean, nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=False)
#     valid_to_date = Column(DateTime, nullable=False)
#     area_id = Column(ForeignKey('areas.id'))
#     large_city_near_id = Column(ForeignKey('areas.id'))
#     publisher_id = Column(ForeignKey('customers.id'))
#
#     area = relationship('Area', primaryjoin='Advertisement.area_id == Area.id')
#     large_city_near = relationship('Area', primaryjoin='Advertisement.large_city_near_id == Area.id')
#     publisher = relationship('Customer')
#
#
# class Blacklist(Base):
#     __tablename__ = 'blacklists'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('blacklists_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     banned_member_id = Column(Integer, nullable=False, index=True)
#     created_at = Column(DateTime, nullable=False)
#     customer_id = Column(ForeignKey('customers.id'))
#
#     customer = relationship('Customer')
#
#
# class UserMediaFile(Base):
#     __tablename__ = 'user_media_files'
#
#     # id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_media_files_id_seq'::regclass)"))
#     id = Column(BigInteger, primary_key=True)
#     member_id = Column(BigInteger, nullable=False, index=True)
#     file = Column(String(100), nullable=False)
#     file_type = Column(Integer, nullable=False)
#     privacy_type = Column(Integer, nullable=False)
#     file_temp_url = Column(String(200), nullable=False)
#     is_archived = Column(Boolean, nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     customer_id = Column(ForeignKey('customers.id'))
#
#     customer = relationship('Customer')
