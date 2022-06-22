from redis import Redis, ConnectionPool
from config import REDIS_URI


def get_redis_client():
    redis_pool = ConnectionPool.from_url(REDIS_URI)
    return Redis(
        connection_pool=redis_pool,
        health_check_interval=10,
        charset="utf-8",
        decode_responses=True
    )


redis_client = get_redis_client()




