from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# from core.tables.models import RedisChannel
from a_del.core.schemas.redis_and_tiers import PremiumTierExpose, RedisChannelExpose


class BaseCustomer(BaseModel):
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    lang: Optional[int]
    premium_tier_id: Optional[PremiumTierExpose]
    redis_channel_id: Optional[RedisChannelExpose]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseCustomer):
    conversation_reference: bytes
    passcode: Optional[str]
    post_header: Optional[bytes]


class CustomerUpdate(BaseCustomer):
    pass


class CustomerExpose(BaseCustomer):
    id: int

    class Config:
        orm_mode = True
