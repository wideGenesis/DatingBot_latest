import uvloop

from core.tables import models
import asyncio


async def fixture():
    await models.PremiumTier(
        tier='free'
    ).save()

    await models.PremiumTier(
        tier='advanced_1m'
    ).save()

    await models.PremiumTier(
        tier='advanced_12m'
    ).save()

    await models.PremiumTier(
        tier='premium_1m'
    ).save()

    await models.PremiumTier(
        tier='premium_12m'
    ).save()

    await models.RedisChannel(
        redis_channel='Україна:Одеська область:Одеса'
    ).save()

    await models.RedisChannel(
        redis_channel='Україна:Київська область:Київ'
    ).save()

    await models.Area(
        area='Україна:Київська область:Київ',
        city='Київ',
        state='Київська область',
        country='Україна',
        is_administrative_center=True
    ).save()

    await models.Area(
        area='Україна:Одеська область:Одеса',
        city='Одеса',
        state='Одеська область',
        country='Україна',
        is_administrative_center=True
    ).save()

    await models.Area(
        area='Україна:Львівська область:Львів',
        city='Львів',
        state='Львівська область',
        country='Україна',
        is_administrative_center=True
    ).save()

    await models.Customer(
        nickname='test_nickname',
        phone=380951112233,
        premium_tier_id=7,
        conversation_reference=bytes('jkgkfgjkjg kjg kjg', 'utf-8'),
        member_id=123456789,
        lang=0,
        is_active=1).save()

    await models.Customer(
        nickname='test_nickname222',
        phone=380951114444,
        premium_tier_id=8,
        conversation_reference=bytes('67676786n6876868n68v56v', 'utf-8'),
        member_id=1000200030,
        lang=1,
        is_active=0
    ).save()

    await models.Advertisement(
        who_for_whom=0,
        prefer_age=2035,
        has_place=1,
        dating_time=1,
        dating_day=0,
        adv_text='F sgt rt yty tr urturtut e ytt5e5yrteuyti yriyeiruyiy',
        phone_is_hidden=1,
        money_support=1,
        redis_channel_id=3,
        is_published=1,
        area_id=4,
        large_city_near_id=4,
        publisher_id=7,
    ).save()

    await models.Advertisement(
        who_for_whom=0,
        prefer_age=3035,
        has_place=0,
        dating_time=0,
        dating_day=1,
        adv_text='fghfds hddg jsfjtyjs gj sgjfyj f ',
        phone_is_hidden=0,
        money_support=1,
        redis_channel_id=2,
        is_published=1,
        area_id=5,
        large_city_near_id=5,
        publisher_id=8,
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
