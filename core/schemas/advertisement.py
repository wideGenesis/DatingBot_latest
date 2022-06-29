from datetime import datetime
from enum import Enum
from typing import Optional, Union, Dict

from pydantic import BaseModel

from core.schemas.customer import CustomerExpose
from core.schemas.area import AreaExpose


class WhoForWhomOptions(int, Enum):
    INCOME = 0
    OUTCOME = 1


class BaseAdvertisement(BaseModel):
    who_for_whom: WhoForWhomOptions
    age: int
    prefer_age: int
    has_place: int
    dating_time: int
    dating_day: int
    adv_text: str
    location: str
    phone_is_hidden: bool
    money_support: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    valid_to_date: datetime
    area_id: Optional[Union[AreaExpose, Dict]]
    large_city_near_id: Optional[Union[AreaExpose, Dict]]
    publisher_id: Optional[Union[CustomerExpose, Dict]]


class AdvertisementCreate(BaseAdvertisement):
    pass


class AdvertisementUpdate(BaseAdvertisement):
    pass


class AdvertisementExpose(BaseAdvertisement):
    id: int
    area_id: int
    large_city_near_id: int
    publisher_id: int
    redis_channel_id: int

    class Config:
        orm_mode = True
