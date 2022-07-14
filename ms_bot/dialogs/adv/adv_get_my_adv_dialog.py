import datetime

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
from botbuilder.schema import Activity, ActivityTypes
import json


from core.tables.models import Area, Advertisement
from helpers.constants import remove_last_message
from settings.logger import CustomLogger
from helpers.copyright import (
    BOT_MESSAGES,
    PREFER_AGE_KB,
    HAS_PLACE_KB,
    DATING_TIME,
    DATING_DAY,
    MONEY_SUPPORT,
)

from ms_bot.bots_models.models import CustomerProfile


logger = CustomLogger.get_logger("bot")


class ListAdvDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(ListAdvDialog, self).__init__(dialog_id or ListAdvDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(TextPrompt.__name__, ListAdvDialog.answer_prompt_validator)
        )
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__, ListAdvDialog.age_prompt_validator)
        )

        self.add_dialog(
            WaterfallDialog(
                "ListAdvDialog",
                [

                    self.get_my_adv_step,
                    self.has_place,
                    self.dating_time,
                    self.dating_day,
                    self.money_support,
                    self.goals,

                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "ListAdvDialog"

    async def get_my_adv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_my_adv_step %s", ListAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        threshold = (datetime.datetime.now() + datetime.timedelta(days=7))
        my_advs = await Advertisement.objects.filter(
            customer=user_data.pk).exclude(
            is_published=False).exclude(
            valid_until_date_gt=threshold).order_by(
            "created_at").all()

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(PREFER_AGE_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            ),
        )

    async def has_place(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("has_place %s", ListAdvDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        result_from_previous_step = str(step_context.context.activity.text).replace('-', '').replace(' ', '')
        user_data.prefer_age = result_from_previous_step

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(HAS_PLACE_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def dating_time(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("dating_time %s", ListAdvDialog.__name__)

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
        user_data.has_place = result_from_previous_step[1]

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(DATING_TIME),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def dating_day(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("dating_day %s", ListAdvDialog.__name__)
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
        user_data.dating_time = result_from_previous_step[1]

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(DATING_DAY),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def money_support(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("money_support %s", ListAdvDialog.__name__)
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
        user_data.dating_day = result_from_previous_step[1]

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(MONEY_SUPPORT),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def goals(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("goals %s", ListAdvDialog.__name__)

        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        money_support = str(step_context.result).split(":")
        money_support = money_support[1]
        if money_support == 'money_yes':
            user_data.money_support = True
        else:
            user_data.money_support = False

        return await step_context.begin_dialog(CreateAdvGoalsDialog.__name__)

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
            "KEY_CALLBACK:man",
            "KEY_CALLBACK:woman",
            "KEY_CALLBACK:both",
            "KEY_CALLBACK:fun",
            "KEY_CALLBACK:relationships",
            "KEY_CALLBACK:dating",
            "KEY_CALLBACK:friendship",
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
            "KEY_CALLBACK:money_yes",
            "KEY_CALLBACK:money_no",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition

    @classmethod
    async def _save_area(cls, user_data):
        area = await Area(area=user_data.area_id)
        try:
            area.save()
            return area

        except UniqueViolationError:
            area = await Area.objects.get(area=user_data.area_id)
            return area

        except Exception:
            logger.exception("Save area to db error %s", user_data.area_id)

        return
