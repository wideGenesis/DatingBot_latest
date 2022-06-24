import asyncio
import json
import pickle
import time

import uvloop

import configuration

from datetime import datetime
from typing import List, Tuple

from aioredis import Redis

from lib.messages import BOT_MESSAGES
from setup.aioredis_client import get_redis_client

from botbuilder.schema import ErrorResponseException

from lib.email_helpers import send_mail
from lib.logger import CustomLogger
from lib.storage_blob_helper import rm_blobs
from setup.db import get_db_cursor
from setup.standalone_bot_adapter import ADAPTER, APP_ID

LOGGING_INTERVAL = 60 * 5  # sec
logger = CustomLogger.get_logger('workers')


async def exclude_customer_if_bot_banned(member_id):
    sql_update = """UPDATE customers
                                SET member_id = NULL,
                                    conversation_reference = NULL,
                                    is_active = 0 
                                WHERE member_id = ?"""
    with get_db_cursor() as cur:
        try:
            cur.execute(sql_update, member_id)
        except Exception:
            logger.exception('DB ERROR WHILE EXCLUDE USER FROM NOTIFICATIONS')

        logger.debug('User: %s excluded from notifications', member_id)


async def send_message_to_tg(member_list: List[Tuple[str, bytes]]):
    for member_id, conversation_reference in member_list:
        try:
            await ADAPTER.continue_conversation(
                pickle.loads(conversation_reference),
                lambda turn_context: turn_context.send_activity(BOT_MESSAGES['incoming_message']),
                APP_ID
            )
            logger.info('Message was sent to ADAPTER user %s', member_id)

        except ErrorResponseException:
            logger.warning('ADAPTER -> Error response code. User: %s', member_id)
            await exclude_customer_if_bot_banned(member_id)
            continue
        except Exception:
            logger.exception('ADAPTER -> Send message error. User: %s', member_id)
            continue

        await asyncio.sleep(5)
    return


async def get_db_customers_by_redis_channel(redis_channel: str):
    sql_select = """SELECT cust.member_id AS member_id,
                           cust.conversation_reference AS conversation_reference
                    FROM customers cust
                    INNER JOIN advertisements adv
                    ON cust.id=publisher_id
                    WHERE adv.redis_channel = %s"""

    logger.debug('Try select customers by redis_channel from db')
    with get_db_cursor() as cur:
        try:
            cur.execute(sql_select, (redis_channel, ))
            db_result = cur.fetchall()
        except Exception:
            logger.exception('DB ERROR')
            return None

    return db_result


# >>>>>>>>>>>>>>>>>>> WORKERS <<<<<<<<<<<<<<<<<<<<<<<<<<
async def consumer(redis_cli: Redis):
    logger.warning('Starting consumer_worker')

    last_logging_time = time.time()
    last_health_time = time.time()

    last_id = 0
    sleep_ms = 5000

    while 1:
        if time.time() - last_logging_time > LOGGING_INTERVAL:
            logger.debug("Waiting for event in notification stream")
            last_logging_time = time.time()

        if time.time() - last_health_time > 30:
            await redis_cli.set(configuration.REDIS_HEALTH_CHECK_KEY, 1)
            await redis_cli.expire(configuration.REDIS_HEALTH_CHECK_KEY, 60)
            last_health_time = time.time()

        try:
            resp = await redis_cli.xread(
                {configuration.STREAM_NOTIFICATION_KEY: last_id},
                count=1,
                block=sleep_ms
            )
        except ConnectionError:
            logger.exception("ERROR REDIS CONNECTION: ")
            continue

        except Exception:
            logger.exception("ERROR REDIS EXCEPTION: ")
            continue

        if not resp:
            continue

        logger.info('Incoming event has occurs, Sending proactive message to all relevant customers')
        key, messages = resp[0]
        last_id, data = messages[0]
        data_dict = {k.decode("utf-8"): data[k].decode("utf-8") for k in data}
        data_dict["id"] = last_id.decode("utf-8")
        data_dict["key"] = key.decode("utf-8")
        # logger.debug('>>>>>>>>>>>>>>>\n%s\n>>>>>>>>>>>>>>>\n', data_dict)

        redis_channel = data_dict.get('redis_channel')
        if redis_channel is None:
            continue
        logger.debug('redis_channel is %s', redis_channel)
        relevant_customers = await get_db_customers_by_redis_channel(redis_channel)

        if relevant_customers is not None:
            await send_message_to_tg(relevant_customers)


async def admin_mail_worker(redis_cli: Redis):
    logger.warning('Starting admin mail worker')
    last_logging_time = time.time()
    last_health_time = time.time()

    while 1:
        if time.time() - last_logging_time > LOGGING_INTERVAL:
            logger.info('Try to get <ADMIN MAIL> from queue')
            last_logging_time = time.time()

        if time.time() - last_health_time > 30:
            await redis_cli.set(configuration.REDIS_HEALTH_CHECK_KEY, 1)
            await redis_cli.expire(configuration.REDIS_HEALTH_CHECK_KEY, 60)
            last_health_time = time.time()

        try:
            result = await redis_cli.lpop(configuration.REDIS_ADMIN_MAIL_QUEUE_KEY)
        except Exception:
            logger.exception('Get message from redis error')
            await asyncio.sleep(5)
            continue

        if result:
            logger.debug('admin mail message FOUND!')

            try:
                message_data = json.loads(result)
                await send_mail(message_data, attach=False)
            except Exception:
                logger.exception('Message proceed error')
        await asyncio.sleep(2)


async def blob_remover_worker(redis_cli: Redis):
    logger.warning('Starting blob_remover_worker')
    last_logging_time = time.time()
    last_health_time = time.time()

    while 1:
        if time.time() - last_logging_time > LOGGING_INTERVAL:
            logger.info('Blob_remover_worker waiting the trigger time')
            last_logging_time = time.time()

        if time.time() - last_health_time > 30:
            await redis_cli.set(configuration.REDIS_HEALTH_CHECK_KEY, 1)
            await redis_cli.expire(configuration.REDIS_HEALTH_CHECK_KEY, 60)
            last_health_time = time.time()

        time_now = datetime.utcnow().replace(microsecond=0)
        hour_now = time_now.hour
        time_trigger = 1 <= hour_now < 2
        minute_now = time_now.minute
        minute_trigger = 10 <= minute_now < 12

        if time_trigger and minute_trigger:
            logger.info('All triggers are true, removing all blobs')
            try:
                rm_blobs()
            except Exception:
                logger.exception('Error while deleting blobs')
                await asyncio.sleep(5)
                continue
        await asyncio.sleep(10)


def run():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    # loop = asyncio.get_event_loop()
    redis_client = get_redis_client()
    logger.info('REDIS CLIENT %s', redis_client)

    asyncio.ensure_future(consumer(redis_client))
    asyncio.ensure_future(admin_mail_worker(redis_client))
    asyncio.ensure_future(blob_remover_worker(redis_client))

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info('Exit\n')

    except Exception:
        logger.exception('Runtime error')


if __name__ == "__main__":
    run()
