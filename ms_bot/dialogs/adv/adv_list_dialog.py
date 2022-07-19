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

from core.tables.models import Area, Advertisement, Customer
from helpers.constants import remove_last_message
from ms_bot.dialogs.location_dialog import RequestLocationDialog
from settings.logger import CustomLogger
from helpers.copyright import (
    BOT_MESSAGES,
    PREFER_AGE_KB,
    LOOKING_FOR_KB,
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
                    self.is_customer_publish_adv_step,
                    self.get_who_for_whom_step,
                    self.get_prefer_age_step,
                    self.get_location_step,
                    self.get_list_of_adv_step,
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "ListAdvDialog"

    async def is_customer_publish_adv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("is_customer_publish_adv_step %s", ListAdvDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        member_id = int(step_context.context.activity.from_property.id)
        # result = await Advertisement.objects.select_related("customer").all()
        result = await Advertisement.objects.select_related("customer").filter(customer__member_id=member_id).all()
        if len(result) == 0:
            await step_context.context.send_activity(BOT_MESSAGES['adv_needed'])
            return await step_context.end_dialog()
        else:
            return await step_context.next([])

    async def get_who_for_whom_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("get_who_for_whom_step %s", ListAdvDialog.__name__)
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
        user_data.search_who_for_whom = result_from_previous_step[1]

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

        result_from_previous_step = str(step_context.context.activity.text).replace('-', '').replace(' ', '')
        user_data.search_prefer_age = result_from_previous_step

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
        search_prefer_age = user_data.search_prefer_age

        redis_channel = f'{result_from_previous_step}/{self_sex}:{search_prefer_age}'

        filtered_adv_s = Advertisement.objects.filter(
            channel=redis_channel).filter(
            is_published=True).filter(
            valid_until_date__lte=datetime.datetime.now()
        ).all()

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(filtered_adv_s),
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

        try:
            int(_value[0]) or int(_value[1])
            if len(_value) == 2:
                condition = 18 <= int(_value[0]) <= 69 and 18 <= int(_value[1]) <= 69

            elif len(_value) == 1:
                condition = 18 <= int(_value[0]) <= 69
            else:
                condition = False

        except ValueError:
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
