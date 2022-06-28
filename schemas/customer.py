from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PremiumTier(BaseModel):
    id: int
    tier: str


class BaseCustomer(BaseModel):
    id: int
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    conversation_reference: bytes
    lang: Optional[int]
    # premium_tier_id: PremiumTier
    # post_header: Optional[bytes]
    is_active: bool
    passcode: Optional[str]
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseCustomer):
    pass


class CustomerUpdate(BaseCustomer):
    pass


class Customer(BaseCustomer):
    id: int
    nickname: str
    phone: int
    email: Optional[EmailStr]
    member_id: int
    lang: Optional[int]
    # premium_tier_id: PremiumTier
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
