from datetime import datetime
from uuid import uuid4
from time import sleep

from setup.redis_client import redis_client

stream_notifications_key = 'notifications'
stream_income_messages_key = 'income_messages'
stream_emails_key = 'emails'
producer = 'bot-framework'
MAX_MESSAGES = 10


def send_data(max_messages):
    count = 0
    while count < max_messages:
        date_time_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        try:
            data = {
                "producer": producer,
                "timestamp": date_time_str,
                "publisher_id": uuid4().hex,
                "redis_channel": '41:50:00',
                "who_for_whom": uuid4().hex,
                "member_id": 430,
                "conv_ref": uuid4().hex,
                "adv_text": uuid4().hex,
                "has_place": uuid4().hex,
                "dating_time": uuid4().hex,
                "dating_day": uuid4().hex,
                "age": 35,
                "prefer_age": 2045,
                "goals": str({
                    "g1": uuid4().hex,
                    "g2": uuid4().hex,
                    "g3": uuid4().hex,
                    "g4": uuid4().hex,
                    "g5": uuid4().hex,
                    "g6": uuid4().hex,
                    "g7": uuid4().hex,
                    "g8": uuid4().hex,
                }),
                "location": uuid4().hex,
                "area_id": uuid4().hex,
                "large_city_near_id": uuid4().hex,
                "phone_is_hidden": uuid4().hex,
                "money_support": uuid4().hex,
                "is_published": uuid4().hex,
                "created_at": uuid4().hex,
            }

            resp = redis_client.xadd(stream_notifications_key, data, maxlen=5)
            print(resp)
            count += 1
            sleep(10)

        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))

        sleep(0.5)


if __name__ == "__main__":
    print('>>>>> redis', redis_client)
    send_data(MAX_MESSAGES)

