import datetime
import random

from asyncpg.exceptions import UniqueViolationError
from faker import Faker
from core.tables.models import Customer, Area, Advertisement, Conversation, Message

# fake = Faker('ua_UA')
fake = Faker('en_US')


async def db_fill_customer(qty):
    for i in range(qty):
        member_id = random.randint(0000000000, 1111111111)
        profile = fake.profile()
        if profile['sex'] == 'M':
            sex = 0
        else:
            sex = 1

        # ############ Area ############

        geo = fake.local_latlng()
        country = geo[3]
        state = geo[4].split('/')
        state = state[1]
        state = state.replace(' ', '_')
        city = str(geo[2]).lower()
        city.replace(' ', '_')
        channel = f'{country}:{state}:{city}'.lower()
        geo = f'{geo[0]}:{geo[1]}'.lower()
        who_for_whom = random.choice(
            [
                'man_to_woman',
                'woman_to_man',
                'any_to_both',
                'man_to_man',
                'woman_to_woman',
                'other_to_other',
                'doesnt_matter',
                'other_to_other']
        )
        area = Area(
            area=channel,
            area_en=channel,
            city=city,
            city_en=city,
            state=state,
            state_en=state,
            country=country,
            country_en=country,
            is_administrative_center=fake.pybool(),
            gps_coordinates_for_adv=geo,
            redis_channel=f"{channel}:{who_for_whom}"
        )
        try:
            area_id = await area.save()
        except UniqueViolationError:
            area_id = await Area.objects.get(area=channel)

        # ############ Customer ############

        customer = Customer(
            nickname=profile['username'],
            phone=int(f'38095{random.randint(0000000, 9999999)}'),
            email=profile['mail'],
            description=fake.paragraph(nb_sentences=1),
            conversation_reference=fake.binary(length=64),
            member_id=member_id,
            lang=random.choice(['en', 'ua', 'es', 'ru']),
            self_sex=sex,
            age=random.randint(18, 69),
            is_active=fake.pybool(),

            hiv_status=random.choice(['pos', 'neg', 'neutral']),
            alco_status=random.choice(['frequently', 'occasionally', 'no']),
            drugs_status=random.choice(['frequently', 'occasionally', 'no']),
            safe_sex_status=random.choice(['always', 'occasionally', 'no']),
            passion_sex=fake.pybool(),
            if_same_sex_position=random.choice(
                ['always_bottom',
                 'vers_common_bottom',
                 'versatile',
                 'vers_common_top',
                 'always_top',
                 'straight',
                 'bi'
                 ]
            ),
            boobs_cock_size=random.choice(['small', 'middle', 'large', 'extra_large']),
            height=random.randint(150, 190),
            weight=random.randint(60, 90),
            premium_tier=random.choice(['free', 'advanced_1m', 'advanced_12m', 'premium_1m', 'premium_12m']),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),


            is_staff=fake.pybool(),
            is_superuser=fake.pybool(),
            is_sport=random.choice(['systematic', 'occasionally', 'no']),
            is_home_or_party=random.choice(['homester', 'gadabout']),
            body_type=random.choice(['slim', 'average', 'fat', 'fitness', 'bodybuilder']),
            is_smoker=fake.pybool(),
            is_tatoo=fake.pybool(),
            is_piercings=fake.pybool(),
            likes=random.randint(10, 1000),
        )

        try:
            customer = await customer.save()
        except UniqueViolationError:
            continue

        #  ############ Advertisement ############

        adv_obj = Advertisement(
            who_for_whom=random.choice(
                ['man_to_woman', 'woman_to_man', 'any_to_both', 'man_to_man', 'woman_to_woman', 'other_to_other']),
            prefer_age=random.randint(1818, 6969),
            has_place=random.choice(['mine', 'sometimes', 'yours', 'fifty_fifty']),
            dating_time=random.choice(['morning', 'day', 'evening', 'night']),
            dating_day=random.choice(['any', 'today', 'weekend']),
            adv_text=fake.paragraph(nb_sentences=1),
            goals=f'{fake.paragraph(nb_sentences=1)}:{fake.paragraph(nb_sentences=1)}',
            phone_is_hidden=fake.pybool(),
            tg_nickname_is_hidden=fake.pybool(),
            email_is_hidden=fake.pybool(),
            money_support=fake.pybool(),
            is_published=fake.pybool(),
            valid_until_date=(datetime.datetime.now() + datetime.timedelta(days=30)),
            redis_channel=area_id.id,
            customer=customer.id,

            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),

        )

        try:
            adv = await adv_obj.save()
        except UniqueViolationError:
            continue

        #  ############ Conversation ############

        conv_obj = Conversation(
            user_one_id=customer.id,
            user_two_id=customer.id - 1,
            created_at=datetime.datetime.utcnow(),
        )

        if i != 1:
            try:
                conv = await conv_obj.save()
            except UniqueViolationError:

                continue
        else:
            conv = 0
        #  ############ Message ############

        if i != 1:
            msg_obj = Message(
                message_text=fake.paragraph(nb_sentences=1),
                sender_id=customer.id,
                conversation=conv.id,
                created_at=datetime.datetime.utcnow(),
            )
            try:
                msg = await msg_obj.save()
            except UniqueViolationError:
                continue
        print('>>> iteration #', i)
