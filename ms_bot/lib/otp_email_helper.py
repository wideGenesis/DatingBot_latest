import json
import logging
import config.conf as conf

from ..lib.email_helpers import build_email_message
from setup.redis_client import redis_client

logger = logging.getLogger('bot')


def otp_send_to_email(recipients: list, otp: str):

    email_message_data = build_email_message(
        recipients,
        otp,
        'otp'
    )
    try:
        redis_client.rpush(conf.REDIS_ADMIN_MAIL_QUEUE_KEY, json.dumps(email_message_data))
    except Exception:
        print('Push to Redis error for otp email %s' % recipients)

    return 'Ok'


