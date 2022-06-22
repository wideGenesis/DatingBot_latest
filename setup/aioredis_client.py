import aioredis
from configuration import REDIS_URI


def get_redis_client():
    redis_cli = aioredis.from_url(REDIS_URI)
    return redis_cli


