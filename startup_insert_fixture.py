import uvloop

from core.tables import models
import asyncio

from helpers.constants import AlcoStatusEnum, DrugsStatusEnum, SafeSexEnum, HivStatusEnum, PremiumTierEnum, HasPlaceEnum


async def fixture():
    # await models.PremiumTier(
    #     tier='free'
    # ).save()
    #
    # await models.PremiumTier(
    #     tier='advanced_1m'
    # ).save()
    #
    # await models.PremiumTier(
    #     tier='advanced_12m'
    # ).save()
    #
    # await models.PremiumTier(
    #     tier='premium_1m'
    # ).save()
    #
    # await models.PremiumTier(
    #     tier='premium_12m'
    # ).save()
    #
    # await models.RedisChannel(
    #     redis_channel='україна:одеська область:одеса'
    # ).save()
    #
    # await models.RedisChannel(
    #     redis_channel='україна:київська область:київ'
    # ).save()
    #
    # await models.Area(
    #     area='україна:київська область:київ',
    #     city='київ',
    #     state='київська область',
    #     country='україна',
    #     is_administrative_center=True
    # ).save()
    #
    # await models.Area(
    #     area='україна:одеська область:одеса',
    #     city='одеса',
    #     state='одеська область',
    #     country='україна',
    #     is_administrative_center=True
    # ).save()
    #
    # await models.Area(
    #     area='україна:львівська область:львів',
    #     city='львів',
    #     state='львівська область',
    #     country='україна',
    #     is_administrative_center=True
    # ).save()

    # await models.Customer(
    #     nickname='test_nickname3333',
    #     phone=380951117676,
    #     premium_tier_id=1,
    #     conversation_reference=bytes('jjhjh hgj hgjk loil;;;es esarsersese strjdfjyhlkgfl', 'utf-8'),
    #     member_id=8111456789,
    #     lang='en',
    #     is_active=1,
    # ).save()
    #
    # await models.Customer(
    #     nickname='test_nickname4444',
    #     phone=380951114545,
    #     conversation_reference=bytes('6str yruiyikuoluiolfjf dftgrtysrdhf,klhf xcbnbvm ', 'utf-8'),
    #     member_id=1111200030,
    #     lang='ua',
    #     is_active=0,
    #     premium_tier_id=1
    # ).save()

    await models.Advertisement(
        who_for_whom='man_to_woman',
        prefer_age=2045,
        has_place=HasPlaceEnum.none.value,
        dating_time='morning',
        dating_day='today',
        adv_text='trutruru  tyikty ou; gtr rcnbvcmv ',
        phone_is_hidden=0,
        money_support=0,
        redis_channel_id=2,
        is_published=1,
        area_id=1,
        large_city_near_id=1,
        publisher_id=2,
    ).save()

    await models.Advertisement(
        who_for_whom='man_to_woman',
        prefer_age=3235,
        has_place=HasPlaceEnum.none.value,
        dating_time='morning',
        dating_day='today',
        adv_text='fjuyiuioutgoi  saretrstyry tseu yyuiutiotuot tui ',
        phone_is_hidden=0,
        money_support=1,
        redis_channel_id=2,
        is_published=1,
        area_id=1,
        large_city_near_id=2,
        publisher_id=1,
    ).save()

    await models.CustomerProfile(
        hiv_status=HivStatusEnum.neg.value,
        alco_status=AlcoStatusEnum.occasionally.value,
        drugs_status=DrugsStatusEnum.frequently.value,
        safe_sex_status=SafeSexEnum.always.value,
        passion_sex=True,
        height=180,
        weight=75,
        is_smoker=True,
        is_tatoo=False,
        customer=1
    ).save()
    await models.CustomerProfile(
        hiv_status=HivStatusEnum.neutral.value,
        alco_status=AlcoStatusEnum.frequently.value,
        drugs_status=DrugsStatusEnum.occasionally.value,
        safe_sex_status=SafeSexEnum.always.value,
        passion_sex=True,
        height=180,
        weight=75,
        is_smoker=True,
        is_tatoo=False,
        customer=2
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
