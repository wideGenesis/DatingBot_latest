import asyncio
import aioredis

redis_address = 'redis://localhost:6379'
redis_input_stream_name = 'input_stream'
redis_output_stream_name = 'event_stream'
redis_rendering_stream_length = int(10)


async def main():
    redis = await aioredis.Redis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)

    for i in range(100):
        items = {'id': i}  # items have to be a dict
        await asyncio.gather(
            redis.xadd(redis_input_stream_name, items, maxlen=redis_rendering_stream_length))
        print(i)


asyncio.run(main())
