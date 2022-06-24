# coding: utf-8
import datetime
import ormar

from typing import Optional, Union, Dict, List

from sqlalchemy import text

from db.engine import METADATA, DATABASE


class ForOrmarMeta(ormar.ModelMeta):
    metadata = METADATA
    database = DATABASE


class User(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'users'

    id: int = ormar.BigInteger(primary_key=True)
    email: Optional[str] = ormar.String(max_length=50, nullable=False, unique=True)
    username: Union[str, int] = ormar.String(max_length=50, nullable=False, unique=True)
    first_name: Optional[str]
    last_name: Optional[str]
    password_hash: str = ormar.String(max_length=1000, nullable=False)
    # groups: Optional[List] =
    # user_permissions: Optional[List] =
    is_staff: bool = ormar.Boolean(nullable=False, server_default=text('False'))
    is_active: bool = ormar.Boolean(nullable=False, server_default=text('True'))
    is_superuser: bool = ormar.Boolean(nullable=False, server_default=text('False'))
    last_login: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    date_joined: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)


class Area(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'areas'

    id: int = ormar.BigInteger(primary_key=True)
    area: str = ormar.String(max_length=200, nullable=False, unique=True)
    city: str = ormar.String(max_length=30, nullable=False)
    state: str = ormar.String(max_length=30, nullable=False)
    country: str = ormar.String(max_length=30, nullable=False)
    is_administrative_center: bool = ormar.Boolean(nullable=False)


class PremiumTier(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'premium_tiers'

    id: int = ormar.BigInteger(primary_key=True)
    tier: str = ormar.Integer(unique=True)


class RedisChannel(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'redis_channels'

    id: int = ormar.BigInteger(primary_key=True)
    redis_channel: str = ormar.String(max_length=200, nullable=False, unique=True)


class Customer(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'customers'

    id: int = ormar.BigInteger(primary_key=True)
    nickname: Optional[str] = ormar.String(max_length=50, nullable=False, unique=True)
    phone: int = ormar.BigInteger(unique=True)
    email: Optional[str] = ormar.String(max_length=100, unique=True)
    conversation_reference: Optional[bytes] = ormar.LargeBinary(max_length=10000)
    member_id: int = ormar.BigInteger(unique=True)
    lang: Optional[int] = ormar.Integer(index=True)
    post_header: Optional[bytes] = ormar.LargeBinary(max_length=10000)
    is_active: bool = ormar.Boolean(nullable=False)
    passcode: Optional[str] = ormar.String(max_length=50)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    premium_tier_id: Optional[Union[PremiumTier, Dict]] = ormar.ForeignKey(PremiumTier)


class Advertisement(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'advertisements'

    id: int = ormar.BigInteger(primary_key=True)
    who_for_whom: int = ormar.Integer(index=True)
    age: int = ormar.Integer(index=True)
    prefer_age: int = ormar.Integer(index=True)
    has_place: int = ormar.Integer(nullable=False)
    dating_time: int = ormar.Integer(nullable=False)
    dating_day: int = ormar.Integer(nullable=False)
    adv_text: str = ormar.Text(nullable=False)
    location: str = ormar.String(max_length=50)
    phone_is_hidden: bool = ormar.Boolean(nullable=False)
    money_support: bool = ormar.Boolean(nullable=False)
    redis_channel_main: str = ormar.String(max_length=100, index=True)
    redis_channel_second: Optional[str] = ormar.String(max_length=100, index=True)
    is_published: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    valid_to_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)),
        nullable=False)
    area_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(Area, related_name="customer_area_id")
    large_city_near_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(Area, related_name="customer_large_city_near_id")
    publisher_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer)


class Blacklist(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'blacklists'

    id: int = ormar.BigInteger(primary_key=True)
    banned_member_id: int = ormar.Integer(nullable=False, index=True)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer)


class UserMediaFile(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'user_media_files'

    id: int = ormar.BigInteger(primary_key=True)
    member_id: int = ormar.BigInteger(index=True)
    file: str = ormar.String(max_length=100, nullable=False)
    file_type: int = ormar.Integer()
    privacy_type: int = ormar.Integer()
    file_temp_url: Optional[str] = ormar.String(max_length=200)
    is_archived: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer)


class AdvGoal(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'adv_goals'

    id: int = ormar.BigInteger(primary_key=True)
    goals_1: Optional[int] = ormar.Integer()
    goals_2: Optional[int] = ormar.Integer()
    goals_3: Optional[int] = ormar.Integer()
    goals_4: Optional[int] = ormar.Integer()
    goals_5: Optional[int] = ormar.Integer()
    goals_6: Optional[int] = ormar.Integer()
    goals_7: Optional[int] = ormar.Integer()
    goals_8: Optional[int] = ormar.Integer()
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    adv_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer)


class Commercial(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'commercial'

    id: int = ormar.BigInteger(primary_key=True)
    title: str = ormar.String(max_length=1000, nullable=False)
    description: str = ormar.String(max_length=1000, nullable=False)
    img: Optional[str] = ormar.String(max_length=100, nullable=False)
    owner: str = ormar.String(max_length=100, nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    valid_to_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)),
        nullable=False)
    is_active: bool = ormar.Boolean(nullable=False)
