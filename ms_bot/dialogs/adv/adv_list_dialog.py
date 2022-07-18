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
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from settings.logger import CustomLogger
from helpers.copyright import (
    BOT_MESSAGES,
    PREFER_AGE_KB,
    HAS_PLACE_KB,
    DATING_TIME,
    DATING_DAY,
    MONEY_SUPPORT, LOOKING_FOR_KB,
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
            RequestLocationDialog(user_state, RequestLocationDialog.__name__)
        )

        self.add_dialog(
            WaterfallDialog(
                "ListAdvDialog",
                [

                    self.get_who_for_whom_step,
                    self.get_prefer_age_step,
                    self.get_has_place_step,
                    self.dating_day,
                    self.money_support,
                    self.goals,

                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "ListAdvDialog"

    async def get_who_for_whom_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_who_for_whom_step %s", ListAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(LOOKING_FOR_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['reprompt']}"),
            ),
        )

    async def get_prefer_age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_prefer_age_step %s", ListAdvDialog.__name__)
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
        user_data.get_who_for_whom = result_from_previous_step[1]


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

    async def get_location_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_location_step %s", ListAdvDialog.__name__)
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
        user_data.get_prefer_sex = result_from_previous_step[1]

        return await step_context.begin_dialog(RequestLocationDialog.__name__)

    async def get_list_of_adv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_list_of_adv_step %s", ListAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        result_from_previous_step = step_context.result
        self_sex = user_data.self_sex
        get_prefer_sex = user_data.get_prefer_age

        redis_channel = f'{result_from_previous_step}/{self_sex}:{get_prefer_sex}'

        filtered_advs = Advertisement.objects.filter(
            channel=redis_channel).filter(
            is_published=True).filter(
            valid_until_date__lte=datetime.datetime.now()
        ).all()

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(filtered_advs),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(f"{BOT_MESSAGES['age_reprompt']}"),
            ),
        )

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
            "KEY_CALLBACK:friendship",

        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
