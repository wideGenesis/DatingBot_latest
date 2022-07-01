import json
import logging
import random
import math

from settings.conf import REDIS_CONF

from helpers.email import build_email_message
from settings.redis_client import redis_client

logger = logging.getLogger("bot")


def generate_otp():
    # storing strings in a list
    digits = [i for i in range(0, 10)]

    # initializing a string
    random_str = ""

    # we can generate any length of string we want
    for i in range(4):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


def otp_send_to_email(recipients: list, otp: str):

    email_message_data = build_email_message(recipients, otp, "otp")
    try:
        redis_client.rpush(
            REDIS_CONF.REDIS_ADMIN_MAIL_QUEUE_KEY, json.dumps(email_message_data)
        )
    except Exception:
        print("Push to Redis error for otp email %s" % recipients)

    return "Ok"
