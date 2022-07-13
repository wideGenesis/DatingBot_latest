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
            is_active=None,
            hiv_status=None,
            alco_status=None,
            drugs_status=None,
            safe_sex_status=None,
            if_same_sex_position=None,
            boobs_cock_size=None,
            height=None,
            weight=None,
            premium_tier=None,
            adv_list=None,  # For adv iter
            created_at=None,
            updated_at=None,
            
            is_staff=None,
            is_superuser=None,
            post_header=None,
            password_hash=None,
            password_hint=None,
            passion_sex=None,
            is_sport=None,
            is_home_or_party=None,
            body_type=None,
            is_smoker=None,
            is_tatoo=None,
            is_piercings=None,
            likes=None,
            instagram_link=None,
            tiktok_link=None,
            
            # Adv
            adv_dict=None,
            adv_pk=None,
            who_for_whom=None,
            global_goals=None,
            prefer_age=None,
            has_place=None,
            dating_time=None,
            dating_day=None,
            adv_text=None,
            goals_list=None,
            phone_is_hidden=None,
            tg_nickname_is_hidden=None,
            email_is_hidden=None,
            money_support=None,
            is_published=None,
            valid_until_date=None,
            redis_channel=None,
            adv_created_at=None,
            adv_updated_at=None,
            
            # Ban
            ban_list=None,
            
            # Files
            files_dict=None,
            file_number=0,
            
            # Other
            authorised=None,
            otp=None,
            temp=None,
            sex_buttons=None,
            relationships_buttons=None,
            walking_buttons=None,
    ):
        self.pk = pk
        self.nickname = nickname
        self.phone = phone
        self.email = email
        self.description = description
        self.conversation_reference = conversation_reference
        self.member_id = member_id
        self.lang = lang
        self.self_sex = self_sex
        self.age = age
        self.is_active = is_active
        self.hiv_status = hiv_status
        self.alco_status = alco_status
        self.drugs_status = drugs_status
        self.safe_sex_status = safe_sex_status
        self.if_same_sex_position = if_same_sex_position
        self.boobs_cock_size = boobs_cock_size
        self.height = height
        self.weight = weight
        self.premium_tier = premium_tier
        self.adv_list = adv_list
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.post_header = post_header
        self.password_hash = password_hash
        self.password_hint = password_hint
        self.passion_sex = passion_sex
        self.is_sport = is_sport
        self.is_home_or_party = is_home_or_party
        self.body_type = body_type
        self.is_smoker = is_smoker
        self.is_tatoo = is_tatoo
        self.is_piercings = is_piercings
        self.likes = likes
        self.instagram_link = instagram_link
        self.tiktok_link = tiktok_link
        self.adv_dict = adv_dict
        self.adv_pk = adv_pk
        self.who_for_whom = who_for_whom
        self.global_goals = global_goals
        self.prefer_age = prefer_age
        self.has_place = has_place
        self.dating_time = dating_time
        self.dating_day = dating_day
        self.adv_text = adv_text
        self.goals_list: list = goals_list
        self.phone_is_hidden = phone_is_hidden
        self.tg_nickname_is_hidden = tg_nickname_is_hidden
        self.email_is_hidden = email_is_hidden
        self.money_support = money_support
        self.is_published = is_published
        self.valid_until_date = valid_until_date
        self.redis_channel = redis_channel
        self.adv_created_at = adv_created_at
        self.adv_updated_at = adv_updated_at
        self.ban_list = ban_list
        self.files_dict = files_dict
        self.file_number = file_number
        self.authorised = authorised
        self.otp = otp
        self.temp = temp
        self.sex_buttons: list = sex_buttons
        self.relationships_buttons: list = relationships_buttons
        self.walking_buttons: list = walking_buttons
