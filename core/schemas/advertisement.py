from datetime import datetime
from enum import Enum
from typing import Optional, Union, Dict, List

from pydantic import BaseModel

from core.schemas.customer import CustomerExpose
from core.schemas.area import AreaExpose
from core.schemas.redis_and_tiers import RedisChannelExpose


class WhoForWhomOptions(int, Enum):
    INCOME = 0
    OUTCOME = 1


class BaseAdvertisement(BaseModel):
    who_for_whom: WhoForWhomOptions
    prefer_age: int
    has_place: int
    dating_time: int
    dating_day: int
    adv_text: str
    phone_is_hidden: bool
    money_support: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    valid_until_date: datetime
    redis_channel_id: Optional[RedisChannelExpose]
    # area_id: Optional[AreaExpose]
    # large_city_near_id: Optional[AreaExpose]
    publisher_id: Optional[Union[CustomerExpose, Dict]]


class AdvertisementCreate(BaseAdvertisement):
    pass


class AdvertisementUpdate(BaseAdvertisement):
    pass


class AdvertisementExpose(BaseAdvertisement):
    id: int

    class Config:
        orm_mode = True
