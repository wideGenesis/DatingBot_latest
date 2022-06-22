import asyncio
import aioredis

redis_address = 'redis://localhost:6379'
redis_input_stream_name = 'input_stream'
redis_output_stream_name = 'output_stream'
redis_rendering_stream_length = int(10)


async def read_stream():
    redis = await aioredis.Redis.from_url(redis_address, encoding='utf-8', decode_responses=True)
    # read first message in stream
    id_ = '0-0'
    while True:
        input_message = await redis.xread(streams={redis_input_stream_name: id_}, count=1)
        if input_message:
            # find id for reading next message
            id_, data = input_message[0][1][0]
            print(input_message[0][1][0][1]['id'])


def main():
    asyncio.run(read_stream())


if __name__ == '__main__':
    main()
