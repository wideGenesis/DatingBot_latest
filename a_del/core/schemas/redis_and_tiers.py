from pydantic import BaseModel


class PremiumTierExpose(BaseModel):
    id: int
    tier: str


class RedisChannelExpose(BaseModel):
    id: int
    redis_channel: str
