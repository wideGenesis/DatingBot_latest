from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


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


class AdvertisementCreate(BaseAdvertisement):
    pass


class AdvertisementUpdate(BaseAdvertisement):
    pass


class Advertisement(BaseAdvertisement):
    id: int
    area_id: int
    large_city_near_id: int
    publisher_id: int
    redis_channel_main: str
    redis_channel_second: str

    class Config:
        orm_mode = True
