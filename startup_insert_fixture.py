import uvloop

from core.tables import models
import asyncio


async def fixture():
    await models.PremiumTier(
        tier='free'
    ).save()

    await models.RedisChannel(
        redis_channel='Україна:Одеська область:Одеса'
    ).save()
    await models.Area(
        area='Україна:Одеська область:Одеса',
        city='Одеса',
        state='Одеська область',
        country='Україна',
        is_administrative_center=True
    ).save()

    await models.Customer(
        nickname='test_nickname',
        phone=380951112233,
        premium_tier_id=1,
        conversation_reference=bytes('jkgkfgjkjg kjg kjg', 'utf-8'),
        member_id=123456789,
        lang=0,
        is_active=1
    ).save()



def run():
    print('Initialize fixture')
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(fixture())

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        print('Exit\n')

    except Exception:
        print('Runtime error')


if __name__ == '__main__':
    run()
