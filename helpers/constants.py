from enum import Enum
from botbuilder.dialogs import WaterfallStepContext
from botbuilder.schema import ErrorResponseException

from helpers.exceptions import DropReply
from ms_bot.bot_helpers.telegram_helper import rm_tg_message


class WhoForWhomEnum(Enum):
    man_to_woman = 0
    woman_to_man = 1
    any_to_both = 2
    man_to_man = 3
    woman_to_woman = 4
    other_to_other = 5


class LangEnum(Enum):
    en = 0
    ua = 1
    es = 2
    ru = 3


class SelfSexEnum(Enum):
    man = 0
    woman = 1


class HasPlaceEnum(Enum):
    none = 0
    yours = 1
    mine = 2
    fifty_fifty = 3


class DatingTimeEnum(Enum):
    morning = 0
    day = 1
    evening = 2
    night = 3


class DatingDayEnum(Enum):
    _any = 0
    today = 1
    weekend = 2


class AdvGoalEnum(Enum):
    dating = 0
    walking = 1
    talking = 2
    relationships = 3
    children = 4
    petting_jerk = 5
    oral_for_me = 6
    oral_for_you = 7
    classic_man_to_woman = 8
    anal_for_me = 9
    anal_for_you = 10
    rim_for_me = 11
    rim_for_you = 12
    fetishes_for_me = 13
    massage_for_me = 14
    massage_for_you = 15
    escorting_for_me = 16
    escorting_for_you = 17


class PremiumTierEnum(Enum):
    free = 0
    advanced_1m = 1
    advanced_12m = 2
    premium_1m = 3
    premium_12m = 4


class PrivacyTypeEnum(Enum):
    open = 0
    hidden = 1


class FileTypeEnum(Enum):
    mp4 = 0
    jpg = 1
    png = 2


class HivStatusEnum(Enum):
    pos = 0
    neg = 1
    neutral = 2


class AlcoStatusEnum(Enum):
    frequently = 'frequently'
    occasionally = 'occasionally'
    no = 'no'


class DrugsStatusEnum(Enum):
    frequently = 'frequently'
    occasionally = 'occasionally'
    no = 'no'


class SafeSexEnum(Enum):
    always = 'always'
    occasionally = 'occasionally'
    no = 'no'


class IfSameSexPositionEnum(Enum):
    always_bottom = 'always_bottom'
    versatile_common_bottom = 'versatile_common_bottom'
    versatile = 'versatile'
    versatile_common_top = 'versatile_common_top'
    always_top = 'always_top'


class BoobsCockSizeEnum(Enum):
    _s = 'small'
    _m = 'middle'
    _l = 'large'
    _xl = 'extra_large'


class IsSportEnum(Enum):
    systemic = 'systemic'
    occasionally = 'occasionally'
    no = 'no'


class IsHomeOrPartyEnum(Enum):
    homester = 'homester'
    gadabout = 'homester'


class BodyTypeEnum(Enum):
    slim = 'slim'
    average = 'average'
    fat = 'fat'
    fitness = 'fitness'
    bodybuilder = 'bodybuilder'


async def remove_last_message(step_context: WaterfallStepContext, callback_query=True):
    if callback_query:
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
    else:
        chat_id = (
            f"{step_context.context.activity.channel_data['message']['chat']['id']}"
        )
        message_id = (
            f"{step_context.context.activity.channel_data['message']['message_id']}"
        )
    try:
        await rm_tg_message(step_context.context, chat_id, message_id)
    except ErrorResponseException as e:
        print(e)
    return


async def remove_reply(step_context: WaterfallStepContext):
    chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
    message_id = f"{step_context.context.activity.channel_data['message']['reply_to_message']['message_id']}"
    await rm_tg_message(step_context.context, chat_id, message_id)
    return


async def remove_last_dropped_message(step_context: WaterfallStepContext):
    chat_id = f"{step_context.context.activity.channel_data['message']['chat']['id']}"
    message_id = (
        f"{step_context.context.activity.channel_data['message']['message_id']}"
    )
    await rm_tg_message(step_context.context, chat_id, message_id)
    return
