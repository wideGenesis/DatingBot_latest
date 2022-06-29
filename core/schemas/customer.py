from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from core.tables.models import RedisChannel


class PremiumTier(BaseModel):
    id: int
    tier: str


class BaseCustomer(BaseModel):
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    conversation_reference: bytes
    lang: Optional[int]
    premium_tier_id: Optional[PremiumTier]
    redis_channel_id: Optional[RedisChannel]
    post_header: Optional[bytes]
    is_active: bool
    passcode: Optional[str]
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseCustomer):
    pass


class CustomerUpdate(BaseCustomer):
    pass


class CustomerExpose(BaseCustomer):
    id: int

    class Config:
        orm_mode = True
