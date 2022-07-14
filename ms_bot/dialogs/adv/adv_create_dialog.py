import datetime
import pickle

from asyncpg import UniqueViolationError
from botbuilder.core import (
    MessageFactory,
    UserState,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
    NumberPrompt,
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes, ErrorResponseException
import json


from core.tables.models import Customer, Advertisement, Area
from helpers.constants import remove_last_message, WhoForWhomEnum
from ms_bot.dialogs.adv.adv_create_goals_dialog import CreateAdvGoalsDialog
from ms_bot.dialogs.adv.adv_create_text_dialog import GetAdvTextDialog
from ms_bot.dialogs.adv.dating.adv_create_dating_dialog import CreateDatingAdvDialog
from settings.logger import CustomLogger
from helpers.copyright import (
    BOT_MESSAGES,
    LOOKING_FOR_KB,
    GLOBAL_GOALS_KB,
    PHONE_IS_HIDDEN,
    TG_IS_HIDDEN,
)

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from ms_bot.dialogs.phone_dialog import RequestPhoneDialog
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class CreateAdvDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(CreateAdvDialog, self).__init__(dialog_id or CreateAdvDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(RequestPhoneDialog(user_state, RequestPhoneDialog.__name__))
        self.add_dialog(
            RequestLocationDialog(user_state, RequestLocationDialog.__name__)
        )
        self.add_dialog(CreateAdvGoalsDialog(user_state, CreateAdvGoalsDialog.__name__))
        self.add_dialog(GetAdvTextDialog(user_state, GetAdvTextDialog.__name__))
        self.add_dialog(CreateDatingAdvDialog(user_state, CreateDatingAdvDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(TextPrompt.__name__, CreateAdvDialog.answer_prompt_validator)
        )
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__, CreateAdvDialog.age_prompt_validator)
        )

        self.add_dialog(
            WaterfallDialog(
                "CreateAdvDialog",
                [
                    self.global_goals,
                    self.who_for_whom,
                    self.processing_step,
                    self.phone_is_hidden,
                    self.tg_nickname_is_hidden,
                    self.adv_text,


                    # self.area_step,
                    # self.parse_area_choice_step,
                    self.member_step,
                    self.request_location_step,
                    self.save_adv,
                    # self.upload_media_step,
                    # self.back_to_parent
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "CreateAdvDialog"

    async def global_goals(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("global_goals %s", CreateAdvDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(GLOBAL_GOALS_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def who_for_whom(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("who_for_whom %s", CreateAdvDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        result_from_previous_step = str(step_context.result).split(":")
        user_data.global_goals = result_from_previous_step[1]

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(LOOKING_FOR_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES["reprompt"]),
            ),
        )

    async def processing_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("processing_step %s", CreateAdvDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        member_id = int(step_context.context.activity.from_property.id)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        for_whom = str(step_context.result).split(":")
        for_whom = for_whom[1]

        customer = await Customer.objects.get_or_none(member_id=member_id)
        if customer is None:
            raise ValueError
        who: str = str(customer.self_sex)

        user_data.who_for_whom = f'{who}:{for_whom}'

        if user_data.global_goals == 'relationships':
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

        if user_data.global_goals == 'dating':
            return await step_context.begin_dialog(CreateDatingAdvDialog.__name__)

        if user_data.global_goals == 'friendship':
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

    async def phone_is_hidden(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("phone_is_hidden %s", CreateAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(PHONE_IS_HIDDEN),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def tg_nickname_is_hidden(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("tg_nickname_is_hidden %s", CreateAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        phone_is_hidden = str(step_context.result).split(":")
        phone_is_hidden = phone_is_hidden[1]
        if phone_is_hidden == 'phone_yes':
            user_data.phone_is_hidden = False
        else:
            user_data.phone_is_hidden = True

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(TG_IS_HIDDEN),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def adv_text(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("adv_text %s", CreateDatingAdvDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        phone_is_hidden = str(step_context.result).split(":")
        phone_is_hidden = phone_is_hidden[1]
        if phone_is_hidden == 'tg_yes':
            user_data.tg_nickname_is_hidden = False
        else:
            user_data.tg_nickname_is_hidden = True
        return await step_context.begin_dialog(GetAdvTextDialog.__name__)

    async def member_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("member_step %s", CreateAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')


        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        member_id = int(step_context.context.activity.from_property.id)
        conversation_reference = pickle.dumps(
            step_context.context.get_conversation_reference(
                step_context.context.activity
            )
        )

        user_data.member_id = member_id
        user_data.conversation_reference = conversation_reference
        user_data.updated_at = datetime.datetime.utcnow()
        user_data.last_seen = user_data.updated_at

        return await step_context.next([])

    async def request_location_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("request_location_step %s", RequestLocationDialog.__name__)
        return await step_context.begin_dialog(RequestLocationDialog.__name__)

    async def save_adv(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("save_new_customer %s", CreateAdvDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        try:
            area = await self._save_area(user_data)
            logger.info("_save_area for %s was successful", user_data.member_id)
        except Exception:
            logger.exception("_save_area for %s was Unsuccessful", user_data.member_id)
            await step_context.context.send_activity("exceptions_occurs")
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

        try:
            await self._save_adv(user_data, area)
            logger.info(
                "_save_adv for %s was successful", user_data.member_id
            )
        except Exception:
            logger.exception(
                "_save_adv for %s was unsuccessful", user_data.member_id
            )
            await step_context.context.send_activity("exceptions_occurs")
            return await step_context.replace_dialog(CreateAdvDialog.__name__)

        return await step_context.next([])

    async def back_to_parent(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug(f"back_to_main from %s", CreateAdvDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await step_context.end_dialog(user_data)

    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text
        _value = _value.strip()
        _value = _value.split("-")

        if len(_value) == 2:
            condition = 18 <= int(_value[0]) <= 69 and 18 <= int(_value[1]) <= 69

        elif len(_value) == 1:
            condition = 18 <= int(_value[0]) <= 69
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:profile_region",
            "KEY_CALLBACK:find_region",
            "KEY_CALLBACK:man",
            "KEY_CALLBACK:woman",
            "KEY_CALLBACK:both",
            "KEY_CALLBACK:friendship",
            "KEY_CALLBACK:relationships",
            "KEY_CALLBACK:dating",
            "KEY_CALLBACK:walking",
            "KEY_CALLBACK:mine",
            "KEY_CALLBACK:sometimes",
            "KEY_CALLBACK:yours",
            "KEY_CALLBACK:fifty_fifty",
            "KEY_CALLBACK:other",
            "KEY_CALLBACK:morning",
            "KEY_CALLBACK:day",
            "KEY_CALLBACK:evening",
            "KEY_CALLBACK:night",
            "KEY_CALLBACK:any",
            "KEY_CALLBACK:today",
            "KEY_CALLBACK:weekend",
            "KEY_CALLBACK:phone_yes",
            "KEY_CALLBACK:phone_no",
            "KEY_CALLBACK:tg_yes",
            "KEY_CALLBACK:tg_no",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition

    @classmethod
    async def _save_area(cls, user_data):
        channel = f'{user_data.area}/{user_data.who_for_whom}'
        tmp_area = user_data.area.split(':')
        country, state, city = tmp_area

        _area = Area(
            area=user_data.area,
            city=city,
            state=state,
            country=country,
            gps_coordinates_for_adv=user_data.gps_coordinates_for_adv,
            redis_channel=channel
        )
        try:
            await _area.save()
            logger.debug('UniqueViolationError %s', _area)
            return _area

        except UniqueViolationError:
            _area = await Area.objects.get_or_none(redis_channel=channel)
            logger.debug('UniqueViolationError %s', _area)
            return _area

        except Exception:
            logger.exception("Save area to db error %s", user_data.area)

        return

    @classmethod
    async def _save_adv(cls, user_data, area):
        customer = await Customer.objects.get_or_none(member_id=user_data.member_id)
        tmp_goals = []
        goals_sorted = ''

        for item in user_data.goals_list:
            goal = item.split(':')
            tmp_goals.append(goal[1])
        tmp_goals.sort()
        for g in tmp_goals:
            goals_sorted += g + ' '

        advertisement = Advertisement(
            who_for_whom=user_data.who_for_whom,
            prefer_age=int(user_data.prefer_age),
            has_place=user_data.has_place,
            dating_time=user_data.dating_time,
            dating_day=user_data.dating_day,
            adv_text=user_data.adv_text,
            goals=goals_sorted,
            phone_is_hidden=user_data.phone_is_hidden,
            tg_nickname_is_hidden=user_data.tg_nickname_is_hidden,
            email_is_hidden=user_data.email_is_hidden,
            money_support=user_data.money_support,
            is_published=True,
            redis_channel=area.id,
            customer=customer.id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        try:
            await advertisement.save()

        except UniqueViolationError:
            await Advertisement.objects.filter(
                member_id=user_data.member_id).update(
                who_for_whom=user_data.who_for_whom,
                prefer_age=int(user_data.prefer_age),
                has_place=user_data.has_place,
                dating_time=user_data.dating_time,
                dating_day=user_data.dating_day,
                adv_text=user_data.adv_text,
                goals=user_data.goals_list,
                phone_is_hidden=user_data.phone_is_hidden,
                tg_nickname_is_hidden=user_data.tg_nickname_is_hidden,
                email_is_hidden=user_data.email_is_hidden,
                money_support=user_data.money_support,
                is_published=True,
                redis_channel=user_data.redis_channel,
                customer=customer.id,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
        except Exception:
            logger.exception("Save customer to db error %s", user_data.member_id)

        return
