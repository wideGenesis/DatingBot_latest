import datetime
import random

from asyncpg.exceptions import UniqueViolationError
from faker import Faker
from core.tables.models import Customer, Area, RedisChannel

# fake = Faker('ua_UA')
fake = Faker('en_US')


async def db_fill_customer(qty):
    for i in range(qty):
        member_id = random.randint(00000000, 11111111)
        profile = fake.profile()
        if profile['sex'] == 'M':
            sex = 0
        else:
            sex = 1
        geo = fake.local_latlng()
        country = geo[3]
        state = geo[4].split('/')
        state = state[1]
        city = str(geo[2]).lower()
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

        redis_channel = RedisChannel(
                redis_channel=channel
        )
        try:
            redis_channel_id = await redis_channel.save()
        except UniqueViolationError:
            redis_channel_id = await RedisChannel.objects.get(redis_channel=channel)

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
            # gps_coordinates=geo,
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

        print('>>> iteration #', i)


