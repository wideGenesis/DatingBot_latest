import datetime
import random

from asyncpg.exceptions import UniqueViolationError
from faker import Faker
from core.tables.models import Customer, Area, RedisChannel, CustomerProfile, Advertisement, PremiumTier

# fake = Faker('ua_UA')
fake = Faker('en_US')


async def premium_tier():
    await PremiumTier(
        tier='free'
    ).save()

    await PremiumTier(
        tier='advanced_1m'
    ).save()

    await PremiumTier(
        tier='advanced_12m'
    ).save()

    await PremiumTier(
        tier='premium_1m'
    ).save()

    await PremiumTier(
        tier='premium_12m'
    ).save()


async def db_fill_customer(qty):
    for i in range(qty):
        member_id = random.randint(0000000000, 1111111111)
        profile = fake.profile()
        if profile['sex'] == 'M':
            sex = 0
        else:
            sex = 1

        ############ Area ############
        print('>>> Area #', i)

        geo = fake.local_latlng()
        country = geo[3]
        state = geo[4].split('/')
        state = state[1]
        state = state.replace(' ', '_')
        city = str(geo[2]).lower()
        city.replace(' ', '_')
        channel = f'{country}:{state}:{city}'.lower()
        geo = f'{geo[0]}:{geo[1]}'.lower()

        area = Area(
            area=channel,
            area_en=channel,
            city=city,
            city_en=city,
            state=state,
            state_en=state,
            country=country,
            country_en=country,
            is_administrative_center=fake.pybool()
        )
        try:
            area_id = await area.save()
        except UniqueViolationError:
            area_id = await Area.objects.get(area=channel)

        ############ RedisChannel ############
        print('>>> RedisChannel #', i)

        redis_channel = RedisChannel(
            redis_channel=channel
        )
        try:
            redis_channel_id = await redis_channel.save()
        except UniqueViolationError:
            redis_channel_id = await RedisChannel.objects.get(redis_channel=channel)

        ############ Customer ############
        print('>>> Customer #', i)

        customer = Customer(
            nickname=profile['username'],
            phone=int(f'38095{random.randint(0000000, 9999999)}'),
            email=profile['mail'],
            description=fake.paragraph(nb_sentences=1),
            conversation_reference=fake.binary(length=64),
            member_id=member_id,
            lang=random.choice(['en', 'ua', 'es', 'ru']),
            self_sex=sex,
            age=str(random.randint(18, 69)),
            is_active=fake.pybool(),
            is_staff=fake.pybool(),
            is_superuser=fake.pybool(),
            gps_coordinates=geo,
            city=area_id.id,
            premium_tier_id=random.choice([1, 2, 3, 4, 5]),
            redis_channel_id=redis_channel_id.id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        try:
            customer = await customer.save()
        except UniqueViolationError:
            customer = await Customer.objects.get(member_id=member_id)

        ############ Customer Profile ############
        print('>>> Customer Profile #', i)

        customer_profile = CustomerProfile(
            hiv_status=random.choice(['pos', 'neg', 'neutral']),
            alco_status=random.choice(['frequently', 'occasionally', 'no']),
            drugs_status=random.choice(['frequently', 'occasionally', 'no']),
            safe_sex_status=random.choice(['always', 'occasionally', 'no']),
            passion_sex=fake.pybool(),
            if_same_sex_position=random.choice(
                ['always_bottom', 'vers_common_bottom', 'versatile', 'vers_common_top', 'always_top']
            ),
            boobs_cock_size=random.choice(['small', 'middle', 'large', 'extra_large']),
            is_sport=random.choice(['systematic', 'occasionally', 'no']),
            is_home_or_party=random.choice(['homester', 'gadabout']),
            body_type=random.choice(['slim', 'average', 'fat', 'fitness', 'bodybuilder']),
            height=random.randint(150, 190),
            weight=random.randint(60, 90),
            is_smoker=fake.pybool(),
            is_tatoo=fake.pybool(),
            is_piercings=fake.pybool(),
            likes=random.randint(10, 1000),

            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            customer=customer.id
        )
        try:
            profile = await customer_profile.save()
        except UniqueViolationError:
            profile = await CustomerProfile.objects.get(customer=customer.id)

        ############ Advertisement ############
        print('>>> Advertisement #', i)

        adv_obj = Advertisement(
            who_for_whom=random.choice(
                ['man_to_woman', 'woman_to_man', 'any_to_both', 'man_to_man', 'woman_to_woman', 'other_to_other']),
            prefer_age=random.randint(1818, 6969),
            has_place=random.choice(['none', 'yours', 'mine', 'fifty_fifty']),
            dating_time=random.choice(['morning', 'day', 'evening', 'night']),
            dating_day=random.choice(['any', 'today', 'weekend']),
            adv_text=fake.paragraph(nb_sentences=1),
            goals=f'{fake.paragraph(nb_sentences=1)}:{fake.paragraph(nb_sentences=1)}',
            phone_is_hidden=fake.pybool(),
            money_support=fake.pybool(),
            is_published=fake.pybool(),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            valid_until_date=(datetime.datetime.now() + datetime.timedelta(days=30)),
            redis_channel_id=redis_channel_id.id,
            area_id=area_id.id,
            large_city_near_id=area_id.id,
            customer=customer.id
        )

        try:
            adv = await adv_obj.save()
        except UniqueViolationError:
            adv = await Advertisement.objects.get(customer=customer.id)

        print('>>> iteration #', i)
