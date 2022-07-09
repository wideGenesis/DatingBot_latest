import datetime
import random

from faker import Faker
from core.tables.models import Customer

# fake = Faker('ua_UA')
fake = Faker('en_US')


def filler():
    fake_customers = []
    for i in range(10):
        # person = fake.person()
        profile = fake.profile()
        # print(person, profile)
        print(profile)
        customer = Customer(
            nickname=fake.nickname(),
            phone=fake.phone_number(),
            email=fake.email(),
            description=fake.lorem(),
            conversation_reference=bytes(fake.lorem()),
            member_id=str(random.randint(00000000, 11111111)),
            lang=random.choice(['en', 'ua', 'es', 'ru']),
            # self_sex=,
            # age=,
            # is_active=,
            # is_staff=,
            # is_superuser=,
            # post_header=,
            # password_hash=,
            # password_hint=,
            # gps_coordinates=,
            # city=,
            # premium_tier_id=,
            # redis_channel_id=,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        customer.save()

if __name__ == '__main__':
    filler()

    """

faker.providers.credit_card
faker.providers.geo
faker.providers.lorem
faker.providers.misc
faker.providers.person
faker.providers.phone_number
faker.providers.profile
faker.providers.ssn
    
    """
