from enum import Enum
from botbuilder.dialogs import WaterfallStepContext
from botbuilder.schema import ErrorResponseException
from ms_bot.bot_helpers.telegram_helper import rm_tg_message


class WhoForWhomEnum(Enum):
    man_to_woman = "man_to_woman"
    woman_to_man = "woman_to_man"
    any_to_both = "any_to_both"
    man_to_man = "man_to_man"
    woman_to_woman = "woman_to_woman"
    other_to_other = "other_to_other"


class LangEnum(Enum):
    en = "en"
    ua = "ua"
    es = "es"
    ru = "ru"


class SelfSexEnum(Enum):
    man = 0
    woman = 1


class HasPlaceEnum(Enum):
    none = "none"
    yours = "yours"
    mine = "mine"
    fifty_fifty = "fifty_fifty"


class DatingTimeEnum(Enum):
    morning = "morning"
    day = "day"
    evening = "evening"
    night = "night"


class DatingDayEnum(Enum):
    _any = "any"
    today = "today"
    weekend = "weekend"


class AdvGoalEnum(Enum):
    dating = "dating"
    walking = "walking"
    talking = "talking"
    relationships = "relationships"
    children = "children"
    petting_jerk = "petting_jerk"
    oral_for_me = "oral_for_me"
    oral_for_you = "oral_for_you"
    classic_man_to_woman = "classic_man_to_woman"
    anal_for_me = "anal_for_me"
    anal_for_you = "anal_for_you"
    rim_for_me = "rim_for_me"
    rim_for_you = "rim_for_you"
    fetishes = "fetishes"
    massage_for_me = "massage_for_me"
    massage_for_you = "massage_for_you"
    escorting_for_me = "escorting_for_me"
    escorting_for_you = "escorting_for_you"


class PremiumTierEnum(Enum):
    free = "free"
    advanced_1m = "advanced_1m"
    advanced_12m = "advanced_12m"
    premium_1m = "premium_1m"
    premium_12m = "premium_12m"


class PrivacyTypeEnum(Enum):
    open = "open"
    hidden = "hidden"


class FileTypeEnum(Enum):
    mp4 = "mp4"
    jpg = "jpg"
    png = "png"


class HivStatusEnum(Enum):
    pos = "pos"
    neg = "neg"
    neutral = "neutral"


class AlcoStatusEnum(Enum):
    frequently = "frequently"
    occasionally = "occasionally"
    no = "no"


class DrugsStatusEnum(Enum):
    frequently = "frequently"
    occasionally = "occasionally"
    no = "no"


class SafeSexEnum(Enum):
    always = "always"
    occasionally = "occasionally"
    no = "no"


class IfSameSexPositionEnum(Enum):
    always_bottom = "always_bottom"
    versatile_common_bottom = "vers_common_bottom"
    versatile = "versatile"
    versatile_common_top = "vers_common_top"
    always_top = "always_top"
    straight = "straight"
    bi = "bi"


class BoobsCockSizeEnum(Enum):
    _s = "small"
    _m = "middle"
    _l = "large"
    _xl = "extra_large"


class IsSportEnum(Enum):
    systemic = "systematic"
    occasionally = "occasionally"
    no = "no"


class IsHomeOrPartyEnum(Enum):
    homester = "homester"
    gadabout = "gadabout"


class BodyTypeEnum(Enum):
    slim = "slim"
    average = "average"
    fat = "fat"
    fitness = "fitness"
    bodybuilder = "bodybuilder"


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
