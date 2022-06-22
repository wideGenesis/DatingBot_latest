"""
It reads the REDIS STREAM events
Using the xread, it gets 1 event per time (from the oldest to the last one)

Usage:
  python consumer.py
"""
import asyncio
import pickle

from setup.db import get_db_cursor
from setup.redis_client import redis_client
from setup.standalone_bot_adapter import ADAPTER, APP_ID

stream_notifications_key = 'notifications'
stream_emails_key = 'emails'
stream_income_messages_key = 'income_messages'
producer = 'producer'
MAX_MESSAGES = 2


async def get_data():
    sql_select = """SELECT c.member_id AS member_id,
                           c.conversation_reference AS conversation_reference
                     FROM customers c
                     WHERE member_id = 1887695430"""  # TODO Not Customer, but adv!!!
    with get_db_cursor() as cur:
        cur.execute(sql_select)
        db_result = cur.fetchall()
        print('db_result >>> ', db_result)

    last_id = 0
    sleep_ms = 5000
    while True:
        try:
            resp = redis_client.xread({stream_notifications_key: last_id}, count=1, block=sleep_ms)
            print("Waiting...")
            if not resp:
                continue
            key, messages = resp[0]
            last_id, data = messages[0]
            data_dict = {k.decode("utf-8"): data[k].decode("utf-8") for k in data}
            data_dict["id"] = last_id.decode("utf-8")
            data_dict["key"] = key.decode("utf-8")
            print('>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>\n', data_dict)
        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))
            continue

        if data_dict.get('redis_channel') == '40:50:00':
            adv_text = data_dict.get('adv_text')
            has_place = data_dict.get('has_place')
            message = f'🔘 Текст объявления: {adv_text}  \n \n' \
                      f'🔘 Место: {has_place}\n'
            for member_id, conversation_reference in db_result:
                try:
                    await ADAPTER.continue_conversation(
                        pickle.loads(conversation_reference),
                        lambda turn_context: turn_context.send_activity(message),
                        APP_ID
                    )
                except Exception:
                    pass


def run():
    loop = asyncio.get_event_loop()

    print('REDIS CLIENT', redis_client)

    asyncio.ensure_future(get_data())

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        print('Exit\n')

    except Exception:
        print('Runtime error')


if __name__ == "__main__":
    print('>>>>> redis', redis_client)
    run()
