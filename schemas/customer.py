from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PremiumTier(BaseModel):
    id: int
    tier: int


class BaseCustomer(BaseModel):
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    conversation_reference: bytes
    lang: Optional[int]
    post_header: Optional[bytes]
    is_active: bool
    passcode: Optional[str]
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseCustomer):
    pass


class CustomerUpdate(BaseCustomer):
    pass


class Customer(BaseCustomer):
    premium_tier_id: PremiumTier

    class Config:
        orm_mode = True
