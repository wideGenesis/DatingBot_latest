# coding: utf-8
import datetime
import ormar

from typing import Optional, Union, Dict, List
from db.engine import METADATA, DATABASE
from helpers.constants import *


class ForOrmarMeta(ormar.ModelMeta):
    metadata = METADATA
    database = DATABASE


class Area(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "areas"

    id: int = ormar.BigInteger(primary_key=True)
    area: Optional[str] = ormar.String(max_length=200, nullable=True, unique=True)
    area_en: Optional[str] = ormar.String(max_length=200, nullable=True, unique=True)

    city: Optional[str] = ormar.String(max_length=30, nullable=True)
    city_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    state: Optional[str] = ormar.String(max_length=30, nullable=True)
    state_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    country: Optional[str] = ormar.String(max_length=30, nullable=True)
    country_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    is_administrative_center: Optional[bool] = ormar.Boolean(nullable=True)


class PremiumTier(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "premium_tiers"

    id: int = ormar.BigInteger(primary_key=True)
    tier: str = ormar.String(
        unique=True, nullable=False, max_length=30, choices=list(PremiumTierEnum)
    )


class RedisChannel(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "redis_channels"

    id: int = ormar.BigInteger(primary_key=True)
    redis_channel: str = ormar.String(unique=True, nullable=False, max_length=200)


class Customer(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "customers"

    id: int = ormar.BigInteger(primary_key=True)
    nickname: Optional[str] = ormar.String(max_length=50, nullable=False, unique=True)
    phone: int = ormar.BigInteger(unique=True)
    email: Optional[str] = ormar.String(max_length=100, unique=True, nullable=True)
    description: Optional[str] = ormar.String(max_length=300, nullable=True)
    conversation_reference: Optional[bytes] = ormar.LargeBinary(max_length=10000)
    member_id: int = ormar.BigInteger(unique=True)
    lang: Optional[int] = ormar.String(max_length=10, choices=list(LangEnum))
    self_sex: Optional[int] = ormar.Integer(choices=list(SelfSexEnum), nullable=True)
    age: Optional[int] = ormar.Integer(nullable=True)
    is_active: bool = ormar.Boolean(nullable=True, default=True)
    is_staff: bool = ormar.Boolean(nullable=True, default=False)
    is_superuser: bool = ormar.Boolean(nullable=True, default=False)
    post_header: Optional[bytes] = ormar.LargeBinary(max_length=10000, nullable=True)
    password_hash: Optional[str] = ormar.String(max_length=50, nullable=True)
    password_hint: Optional[str] = ormar.String(max_length=50, nullable=True)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    gps_coordinates: Optional[str] = ormar.String(max_length=50, nullable=True)

    city: Optional[Union[Area, Dict]] = ormar.ForeignKey(Area, related_name="rel_city")
    premium_tier_id: Optional[PremiumTier] = ormar.ForeignKey(
        PremiumTier, related_name="rel_premium_tier"
    )
    redis_channel_id: Optional[Union[RedisChannel, Dict]] = ormar.ForeignKey(
        RedisChannel, related_name="rel_redis_channel_from_customer"
    )


class CustomerProfile(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "customer_profiles"

    id: int = ormar.BigInteger(primary_key=True)
    hiv_status: Optional[str] = ormar.String(
        nullable=True, choices=list(HivStatusEnum), max_length=20
    )
    alco_status: Optional[str] = ormar.String(
        nullable=True, choices=list(AlcoStatusEnum), max_length=20
    )
    drugs_status: Optional[str] = ormar.String(
        nullable=True, choices=list(DrugsStatusEnum), max_length=20
    )
    safe_sex_status: Optional[str] = ormar.String(
        nullable=True, choices=list(SafeSexEnum), max_length=20
    )
    passion_sex: Optional[bool] = ormar.Boolean(nullable=True)
    if_same_sex_position: Optional[str] = ormar.String(
        nullable=True, choices=list(IfSameSexPositionEnum), max_length=20
    )
    boobs_cock_size: Optional[str] = ormar.String(
        nullable=True, choices=list(BoobsCockSizeEnum), max_length=20
    )
    is_sport: Optional[str] = ormar.String(
        nullable=True, choices=list(IsSportEnum), max_length=20
    )
    is_home_or_party: Optional[str] = ormar.String(
        nullable=True, choices=list(IsHomeOrPartyEnum), max_length=20
    )
    body_type: Optional[str] = ormar.String(
        nullable=True, choices=list(BodyTypeEnum), max_length=20
    )
    height: int = ormar.Integer(nullable=True)
    weight: int = ormar.Integer(nullable=True)
    is_smoker: Optional[bool] = ormar.Boolean(nullable=True)
    is_tatoo: Optional[bool] = ormar.Boolean(nullable=True)
    is_piercings: Optional[bool] = ormar.Boolean(nullable=True)
    likes: Optional[int] = ormar.Integer(nullable=True)
    instagram_link: Optional[str] = ormar.String(
        index=True, max_length=50, unique=True, nullable=True
    )
    tiktok_link: Optional[str] = ormar.String(
        index=True, max_length=50, unique=True, nullable=True
    )
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    customer: Optional[Customer] = ormar.ForeignKey(Customer, unique=True)


class Advertisement(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "advertisements"

    id: int = ormar.BigInteger(primary_key=True)
    who_for_whom: str = ormar.String(max_length=50, choices=list(WhoForWhomEnum))
    prefer_age: int = ormar.Integer(index=True)
    has_place: str = ormar.String(
        max_length=50, nullable=False, choices=list(HasPlaceEnum)
    )
    dating_time: str = ormar.String(
        max_length=50, nullable=False, choices=list(DatingTimeEnum)
    )
    dating_day: str = ormar.String(
        nullable=False, max_length=50, choices=list(DatingDayEnum)
    )

    adv_text: str = ormar.Text(nullable=False)
    goals: str = ormar.String(nullable=False, max_length=1000)
    phone_is_hidden: bool = ormar.Boolean(nullable=False)
    money_support: bool = ormar.Boolean(nullable=False)
    is_published: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    valid_until_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)), nullable=False
    )
    redis_channel_id: Optional[Union[RedisChannel, Dict]] = ormar.ForeignKey(
        RedisChannel, related_name="rel_redis_channel_from_adv"
    )
    area_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(
        Area, related_name="rel_area_id"
    )
    large_city_near_id: Optional[Union[Area, Dict]] = ormar.ForeignKey(
        Area, related_name="rel_large_city_near_id"
    )
    customer: Optional[Customer] = ormar.ForeignKey(Customer, unique=False, related_name="rel_customer_from_adv")


class Blacklist(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "blacklists"

    id: int = ormar.BigInteger(primary_key=True)
    banned_member_id: int = ormar.Integer(nullable=False, index=True)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(
        Customer, related_name="rel_customer_from_blacklist"
    )


class UserMediaFile(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "user_media_files"

    id: int = ormar.BigInteger(primary_key=True)
    # member_id: int = ormar.BigInteger(index=True)
    file: str = ormar.String(max_length=200, nullable=False)
    file_type: int = ormar.String(max_length=20, choices=list(FileTypeEnum))
    privacy_type: int = ormar.String(max_length=20, choices=list(PrivacyTypeEnum))
    is_archived: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=True
    )
    customer_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(
        Customer, related_name="rel_customer_from_usermediafile"
    )


class Message(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "messages"

    id: int = ormar.BigInteger(primary_key=True)
    from_member_id: int = ormar.BigInteger(index=True)
    to_member_id: int = ormar.BigInteger(index=True)
    message_text: str = ormar.String(max_length=1000, nullable=False)
    is_read: bool = ormar.Boolean(nullable=False)
    send_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    sender_id: Union[Customer, Dict] = ormar.ForeignKey(
        Customer, related_name="rel_sender_id"
    )
    recipient_id: Union[Customer, Dict] = ormar.ForeignKey(
        Customer, related_name="rel_recipient_id"
    )
    is_seen: bool = ormar.Boolean(nullable=False)
    sender_avatar: Optional[Union[UserMediaFile, Dict]] = ormar.ForeignKey(
        Customer, related_name="rel_sender_avatar"
    )
    recipient_avatar: Optional[Union[UserMediaFile, Dict]] = ormar.ForeignKey(
        Customer, related_name="rel_recipient_avatar"
    )


class Conversation(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "conversations"

    id: int = ormar.BigInteger(primary_key=True)
    conversation_name: str = ormar.String(max_length=20, nullable=False)


# class AdvGoal(ormar.Model):
#     class Meta(ForOrmarMeta):
#         tablename: str = "adv_goals"
#
#     id: int = ormar.BigInteger(primary_key=True)
#
#     goals_1: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_2: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_3: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_4: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_5: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_6: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_7: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     goals_8: Optional[str] = ormar.String(max_length=50, choices=list(AdvGoalEnum))
#     created_at: datetime.datetime = ormar.DateTime(
#         default=datetime.datetime.now, nullable=False
#     )
#     adv_id: Optional[Union[Customer, Dict]] = ormar.ForeignKey(
#         Advertisement, related_name="rel_adv"
#     )


class Commercial(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "commercial"

    id: int = ormar.BigInteger(primary_key=True)
    title: str = ormar.String(max_length=1000, nullable=False)
    description: str = ormar.String(max_length=1000, nullable=False)
    img: Optional[str] = ormar.String(max_length=100, nullable=False)
    owner: str = ormar.String(max_length=100, nullable=False)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    valid_to_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)), nullable=False
    )
    is_active: bool = ormar.Boolean(nullable=False)
