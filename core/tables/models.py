# coding: utf-8
import datetime
import ormar

from typing import Optional, Union, Dict, List
from sqlalchemy import text
from db.engine import METADATA, DATABASE
from enum import Enum


class WhoForWhomEnum(Enum):
    man_to_woman = 0
    woman_to_man = 1
    any_to_both = 2
    man_to_man = 3
    woman_to_woman = 4
    other_to_other = 5


class LangEnum(Enum):
    en = 0
    ua = 1
    es = 2
    ru = 3


class HasPlaceEnum(Enum):
    none = 0
    yours = 1
    mine = 2
    fifty_fifty = 3


class DatingTime(Enum):
    morning = 0
    day = 1
    evening = 2
    night = 3


class DatingDay(Enum):
    _any = 0
    today = 1
    weekend = 2


class AdvGoalEnum(Enum):
    dating = 0
    walking = 1
    talking = 2
    relationships = 3
    children = 4
    petting_jerk = 5
    oral_for_me = 6
    oral_for_you = 7
    classic_man_to_woman = 8
    anal_for_me = 9
    anal_for_you = 10
    rim_for_me = 11
    rim_for_you = 12
    fetishes_for_me = 13
    massage_for_me = 14
    massage_for_you = 15
    escorting_for_me = 16
    escorting_for_you = 17


class PremiumTierEnum(Enum):
    free = 0
    advanced_1m = 1
    advanced_12m = 2
    premium_1m = 3
    premium_12m = 4


class PrivacyTypeEnum(Enum):
    open = 0
    hidden = 1


class FileTypeEnum(Enum):
    mp4 = 0
    jpg = 1
    png = 2


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
    tier: int = ormar.Integer(unique=True, nullable=False, choices=list(PremiumTierEnum))


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
    email: Optional[str] = ormar.String(max_length=100, unique=True, nullable=True)
    conversation_reference: Optional[bytes] = ormar.LargeBinary(max_length=10000)
    member_id: int = ormar.BigInteger(unique=True)
    lang: Optional[int] = ormar.Integer(index=True, choices=list(LangEnum))
    instagram_link: Optional[str] = ormar.String(index=True, max_length=50, unique=True, nullable=True)
    tiktok_link: Optional[str] = ormar.String(index=True, max_length=50, unique=True, nullable=True)
    is_active: bool = ormar.Boolean(nullable=False)
    post_header: Optional[bytes] = ormar.LargeBinary(max_length=10000, nullable=True)
    passcode: Optional[str] = ormar.String(max_length=50, nullable=True)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    premium_tier_id: Optional[Union[PremiumTier, Dict]] = ormar.ForeignKey(
        PremiumTier, related_name='rel_premium_tier'
    )
    redis_channel_id: Optional[Union[RedisChannel, Dict]] = ormar.ForeignKey(
        RedisChannel, related_name='rel_redis_channel_from_customer'
    )


class Advertisement(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'advertisements'

    id: int = ormar.BigInteger(primary_key=True)
    who_for_whom: int = ormar.Integer(index=True, choices=list(WhoForWhomEnum))
    age: int = ormar.Integer(index=True)
    prefer_age: int = ormar.Integer(index=True)
    has_place: int = ormar.Integer(nullable=False, choices=list(HasPlaceEnum))
    dating_time: int = ormar.Integer(nullable=False, choices=list(DatingTime))
    dating_day: int = ormar.Integer(nullable=False, choices=list(DatingDay))
    adv_text: str = ormar.Text(nullable=False)
    location: str = ormar.String(max_length=50)
    phone_is_hidden: bool = ormar.Boolean(nullable=False)
    money_support: bool = ormar.Boolean(nullable=False)
    is_published: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    valid_to_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)),
        nullable=False)
    redis_channel_id: Optional[Union[RedisChannel, Dict]] = ormar.ForeignKey(
        RedisChannel, related_name='rel_redis_channel_from adv'
    )
    area_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(
        Area, related_name='rel_area_id'
    )
    large_city_near_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(
        Area, related_name='rel_large_city_near_id'
    )
    publisher_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer, related_name='rel_publisher')


class Blacklist(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'blacklists'

    id: int = ormar.BigInteger(primary_key=True)
    banned_member_id: int = ormar.Integer(nullable=False, index=True)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(
        Customer, related_name='rel_customer_from_blacklist'
    )


class UserMediaFile(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'user_media_files'

    id: int = ormar.BigInteger(primary_key=True)
    # member_id: int = ormar.BigInteger(index=True)
    file: str = ormar.String(max_length=200, nullable=False)
    file_type: int = ormar.Integer(choices=list(FileTypeEnum))
    privacy_type: int = ormar.Integer(choices=list(PrivacyTypeEnum))
    is_archived: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(
        Customer, related_name='rel_customer_from_usermediafile'
    )


class AdvGoal(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = 'adv_goals'

    id: int = ormar.BigInteger(primary_key=True)
    goals_1: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_2: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_3: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_4: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_5: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_6: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_7: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    goals_8: Optional[int] = ormar.Integer(choices=list(AdvGoalEnum))
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, nullable=False)
    adv_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Advertisement, related_name='rel_adv')


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
