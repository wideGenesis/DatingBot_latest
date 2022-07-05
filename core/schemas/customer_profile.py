from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.tables.models import Customer


class BaseCustomerProfile(BaseModel):
    hiv_status: Optional[str]
    alco_status: Optional[str]
    drugs_status: Optional[str]
    safe_sex_status: Optional[str]
    passion_sex: Optional[bool]
    if_same_sex_position: Optional[str]
    boobs_cock_size: Optional[str]
    is_sport: Optional[str]
    is_home_or_party: Optional[str]
    body_type: Optional[str]
    height: int
    weight: int
    is_smoker: Optional[bool]
    is_tatoo: Optional[bool]
    is_piercings: Optional[bool]
    likes: Optional[int]
    instagram_link: Optional[str]
    tiktok_link: Optional[str]
    created_at: datetime
    updated_at: datetime


class CustomerProfileCreate(BaseCustomerProfile):
    pass


class CustomerProfileUpdate(BaseCustomerProfile):
    pass


class CustomerProfileExpose(BaseCustomerProfile):
    id: int
    customer: Optional[Customer]

    class Config:
        orm_mode = True
