from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# from core.tables.models import RedisChannel
from core.schemas.redis_and_tiers import PydanticPremiumTier, PydanticRedisChannel


class BaseCustomer(BaseModel):
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    conversation_reference: bytes
    lang: Optional[int]
    premium_tier_id: Optional[PydanticPremiumTier]
    redis_channel_id: Optional[PydanticRedisChannel]
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
