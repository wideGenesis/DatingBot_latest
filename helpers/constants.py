from enum import Enum
from botbuilder.dialogs import WaterfallStepContext

from helpers.exceptions import DropReply
from ms_bot.bot_helpers.telegram_helper import rm_tg_message


class ChannelMessenger(Enum):
    tg = 'telegram'
    viber = 'viber'


async def remove_last_message(step_context: WaterfallStepContext, callback_query=True):
    if callback_query:
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
    else:
        chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['message']['message_id']}"
    await rm_tg_message(step_context.context, chat_id, message_id)
    return


async def remove_reply(step_context: WaterfallStepContext):
    chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
    message_id = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"
    await rm_tg_message(step_context.context, chat_id, message_id)
    return


async def remove_last_dropped_message(step_context: WaterfallStepContext):
    chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
    message_id = f"{step_context.context.activity.channel_data['message']['message_id']}"
    await rm_tg_message(step_context.context, chat_id, message_id)
    return
