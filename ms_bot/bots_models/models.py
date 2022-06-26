from datetime import datetime
from dataclasses import dataclass


@dataclass
class CustomerProfile:
    def __init__(
            self,
            # Customer
            pk=None,
            nickname=None,
            phone=None,
            email=None,
            premium_tier=None,
            conversation_reference=None,
            member_id=None,
            lang=None,
            self_sex=None,
            age=None,

            post_header=None,
            is_active=None,
            created_at=None,
            updated_at=None,
            personal_profile=None,
            sex_profile=None,
            passcode=None,
            
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

            # Other
            authorised=None,
            otp=None,
            temp=None
            
    ):
        self.temp = temp
        self.otp: int = otp
        self.authorised: int = authorised
        self.files_dict = files_dict
        self.ban_list: list = ban_list
        self.redis_channel: str = redis_channel
        self.money_support: int = money_support
        self.phone_is_hidden: int = phone_is_hidden
        self.large_city_near_id: int = large_city_near_id
        self.area_id: int = area_id
        self.location: str = location
        self.adv_text: str = adv_text
        self.dating_day: int = dating_day
        self.dating_time: int = dating_time
        self.has_place: int = has_place
        self.prefer_age: int = prefer_age
        self.age: int = age
        self.who_for_whom: int = who_for_whom
        self.adv_pk: int = adv_pk
        self.adv_dict: dict = adv_dict
        self.passcode: str = passcode
        self.sex_profile: int = sex_profile
        self.personal_profile: int = personal_profile
        self.updated_at: datetime = updated_at
        self.created_at: datetime = created_at
        self.is_active: int = is_active
        self.post_header: str = post_header
        self.self_sex: int = self_sex
        self.lang: int = lang
        self.member_id: int = member_id
        self.conversation_reference = conversation_reference
        self.premium_tier: int = premium_tier
        self.email: str = email
        self.phone: int = phone
        self.nickname: str = nickname
        self.pk: int = pk

        

