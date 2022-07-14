# coding: utf-8
import datetime
from uuid import UUID

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
    area: Optional[str] = ormar.String(max_length=200, nullable=True, unique=False)
    area_en: Optional[str] = ormar.String(max_length=200, nullable=True, unique=False)

    city: Optional[str] = ormar.String(max_length=30, nullable=True)
    city_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    state: Optional[str] = ormar.String(max_length=30, nullable=True)
    state_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    country: Optional[str] = ormar.String(max_length=30, nullable=True)
    country_en: Optional[str] = ormar.String(max_length=30, nullable=True)

    is_administrative_center: Optional[bool] = ormar.Boolean(nullable=True)
    gps_coordinates_for_adv: Optional[str] = ormar.String(max_length=50, nullable=True)
    redis_channel: str = ormar.String(unique=True, nullable=False, max_length=200)


class Customer(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "customers"

    #  major fields
    id: int = ormar.BigInteger(primary_key=True)

    nickname: Optional[str] = ormar.String(max_length=50, nullable=False, unique=True)
    phone: int = ormar.BigInteger(unique=True)
    email: Optional[str] = ormar.String(max_length=100, unique=True, nullable=True)

    description: Optional[str] = ormar.String(max_length=300, nullable=True)
    conversation_reference: bytes = ormar.LargeBinary(max_length=10000)
    member_id: int = ormar.BigInteger(unique=True)
    lang: Optional[str] = ormar.String(max_length=10, choices=list(LangEnum))
    self_sex: Optional[str] = ormar.String(max_length=10, choices=list(SelfSexEnum))
    age: Optional[int] = ormar.Integer(nullable=True)
    is_active: bool = ormar.Boolean(nullable=True, default=True)

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

    if_same_sex_position: Optional[str] = ormar.String(
        nullable=True, choices=list(IfSameSexPositionEnum), max_length=20
    )
    boobs_cock_size: Optional[str] = ormar.String(
        nullable=True, choices=list(BoobsCockSizeEnum), max_length=20
    )
    height: Optional[int] = ormar.Integer(nullable=True)
    weight: Optional[int] = ormar.Integer(nullable=True)
    premium_tier: Optional[str] = ormar.String(
        nullable=True, choices=list(PremiumTierEnum), max_length=30
    )
    adv_list: Optional[str] = ormar.JSON(nullable=True)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )

    # minor fields
    is_staff: bool = ormar.Boolean(nullable=True, default=False)
    is_superuser: bool = ormar.Boolean(nullable=True, default=False)
    post_header: Optional[bytes] = ormar.LargeBinary(max_length=10000, nullable=True)
    password_hash: Optional[str] = ormar.String(max_length=50, nullable=True)
    password_hint: Optional[str] = ormar.String(max_length=50, nullable=True)
    passion_sex: Optional[bool] = ormar.Boolean(nullable=True)
    is_sport: Optional[str] = ormar.String(
        nullable=True, choices=list(IsSportEnum), max_length=20
    )
    is_home_or_party: Optional[str] = ormar.String(
        nullable=True, choices=list(IsHomeOrPartyEnum), max_length=20
    )
    body_type: Optional[str] = ormar.String(
        nullable=True, choices=list(BodyTypeEnum), max_length=20
    )
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
    goals: str = ormar.String(nullable=False, max_length=2000)

    phone_is_hidden: bool = ormar.Boolean(nullable=False)
    tg_nickname_is_hidden: bool = ormar.Boolean(nullable=False)
    email_is_hidden: Optional[bool] = ormar.Boolean(nullable=True)

    money_support: bool = ormar.Boolean(nullable=False)
    is_published: bool = ormar.Boolean(nullable=False)
    valid_until_date: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=7)), nullable=False
    )

    redis_channel: Optional[Area] = ormar.ForeignKey(Area)
    customer: Optional[Customer] = ormar.ForeignKey(Customer, unique=False)

    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )


class Blacklist(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "blacklists"

    id: int = ormar.BigInteger(primary_key=True)
    banned_member_id: int = ormar.Integer(nullable=False, index=True)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    customer: Optional[Union[Customer, Dict]] = ormar.ForeignKey(Customer)


class UserMediaFile(ormar.Model):
    class Meta(ForOrmarMeta):
        tablename: str = "user_media_files"

    id: int = ormar.BigInteger(primary_key=True)
    file: str = ormar.String(max_length=200, nullable=False)
    file_type: str = ormar.String(max_length=20, choices=list(FileTypeEnum))
    privacy_type: str = ormar.String(max_length=20, choices=list(PrivacyTypeEnum))
    is_archived: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, nullable=True
    )
    customer: Customer = ormar.ForeignKey(Customer)


# class Conversation(ormar.Model):
#     class Meta(ForOrmarMeta):
#         tablename: str = "conversations"
#
#     id: int = ormar.BigInteger(primary_key=True)
#     user_one_id: Customer = ormar.ForeignKey(Customer, related_name='user_one_id')
#     user_two_id: Customer = ormar.ForeignKey(Customer, related_name='user_two_id')
#     created_at: datetime.datetime = ormar.DateTime(
#         default=datetime.datetime.now, nullable=False
#     )
#
#
# class Message(ormar.Model):
#     class Meta(ForOrmarMeta):
#         tablename: str = "messages"
#
#     id: int = ormar.BigInteger(primary_key=True)
#     message_text: str = ormar.String(max_length=1000, nullable=False)
#     sender_id: Customer = ormar.ForeignKey(Customer, related_name='sender_id')
#     conversation: Conversation = ormar.ForeignKey(Conversation, related_name='conversation')
#     created_at: datetime.datetime = ormar.DateTime(
#         default=datetime.datetime.now, nullable=False
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
