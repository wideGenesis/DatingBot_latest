import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerProfile:  # TODO match to db model
    def __init__(
            self,
            # Customer
            pk=None,
            nickname=None,
            phone=None,
            email=None,
            description=None,
            conversation_reference=None,
            member_id=None,
            lang=None,
            self_sex=None,
            age=None,
            instagram_link=None,
            tiktok_link=None,
            is_active=None,
            is_staff=None,
            is_superuser=None,
            post_header=None,
            password_hash=None,
            password_hint=None,
            likes=None,
            created_at=None,
            updated_at=None,
            gps_coordinates=None,
            city=None,
            premium_tier=None,
            redis_channel_id=None,

            personal_profile_dict=None,
            sex_profile_dict=None,

            # Adv
            adv_dict=None,
            adv_pk=None,
            who_for_whom=None,
            prefer_age=None,
            has_place=None,
            dating_time=None,
            dating_day=None,
            adv_text=None,
            location=None,
            area_id=None,
            large_city_near_id=None,
            phone_is_hidden=None,
            money_support=None,
            redis_channel=None,
            # Ban
            ban_list=None,
            # Files
            files_dict=None,
            file_number=0,
            # Other
            authorised=None,
            otp=None,
            temp=None,
    ):
        self.temp = temp
        self.otp = otp
        self.authorised = authorised
        self.file_number = file_number
        self.files_dict = files_dict
        self.ban_list = ban_list
        self.redis_channel = redis_channel
        self.money_support = money_support
        self.phone_is_hidden = phone_is_hidden
        self.large_city_near_id = large_city_near_id
        self.area_id = area_id
        self.location = location
        self.adv_text = adv_text
        self.dating_day = dating_day
        self.dating_time = dating_time
        self.has_place = has_place
        self.prefer_age = prefer_age
        self.who_for_whom = who_for_whom
        self.adv_pk = adv_pk
        self.adv_dict = adv_dict
        self.sex_profile_dict = sex_profile_dict
        self.personal_profile_dict = personal_profile_dict
        self.redis_channel_id = redis_channel_id
        self.premium_tier = premium_tier
        self.city = city
        self.gps_coordinates: Optional[str] = gps_coordinates
        self.updated_at: datetime.datetime = updated_at
        self.created_at: datetime.datetime = created_at
        self.likes: Optional[int] = likes
        self.password_hint: Optional[str] = password_hint
        self.password_hash: Optional[str] = password_hash
        self.post_header: Optional[bytes] = post_header
        self.is_superuser: bool = is_superuser
        self.is_staff: bool = is_staff
        self.is_active: bool = is_active
        self.tiktok_link: Optional[str] = tiktok_link
        self.instagram_link: Optional[str] = instagram_link
        self.age: Optional[int] = age
        self.self_sex: Optional[int] = self_sex
        self.lang: Optional[int] = lang
        self.member_id: int = member_id
        self.conversation_reference = conversation_reference
        self.description: Optional[str] = description
        self.email: Optional[str] = email
        self.phone: int = phone
        self.nickname: Optional[str] = nickname
        self.pk: int = pk
