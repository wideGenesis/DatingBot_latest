from pydantic import BaseModel


class PydanticPremiumTier(BaseModel):
    id: int
    tier: str


class PydanticRedisChannel(BaseModel):
    id: int
    redis_channel: str
