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

# from profanity_filter import ProfanityFilter
from helpers.constants import remove_last_message
from settings.logger import CustomLogger
from helpers.copyright import (
    LOOKING_FOR_KB,
    goals_kb,
    BOT_MESSAGES,
)

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class CreateAdvGoalsDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(CreateAdvGoalsDialog, self).__init__(
            dialog_id or CreateAdvGoalsDialog.__name__
        )

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            TextPrompt(
                TextPrompt.__name__, CreateAdvGoalsDialog.answer_prompt_validator
            )
        )
        self.add_dialog(
            WaterfallDialog(
                "CreateAdvGoalsDialog",
                [
                    self.loop_step,
                    self.post_loop_step,

                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "CreateAdvGoalsDialog"
        self.goals_type = None
        self.goals_buttons = None

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("loop_step %s", CreateAdvGoalsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        if user_data.global_goals == 'relationships':
            self.goals_buttons = user_data.relationships_buttons
        elif user_data.global_goals == 'dating':
            self.goals_buttons = user_data.sex_buttons
        elif user_data.global_goals == 'walking':
            self.goals_buttons = user_data.walking_buttons
        else:
            raise ValueError

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
                    channel_data=json.dumps(goals_kb(self.goals_buttons)),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def post_loop_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("post_loop_step %s", CreateAdvGoalsDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        result_from_previous_step = str(step_context.result).split(':')
        result_from_previous_step = result_from_previous_step[1]
        sex_buttons = user_data.sex_buttons

        for item in sex_buttons:
            if item[0]['callback_data'] == 'ready':
                return await step_context.end_dialog()

            if item[0]['callback_data'] == result_from_previous_step:
                index = sex_buttons.index(item)
                sex_buttons.pop(index)
                user_data.sex_buttons = sex_buttons

                if user_data.goals_list is None:
                    user_data.goals_list = [result_from_previous_step]

                else:
                    user_data.goals_list.append(result_from_previous_step)

                return await step_context.replace_dialog(CreateAdvGoalsDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:petting",
            "KEY_CALLBACK:oral_to_me",
            "KEY_CALLBACK:oral_to_you",
            "KEY_CALLBACK:hetero_fuck",
            "KEY_CALLBACK:anal_to_you",
            "KEY_CALLBACK:anal_to_me",
            "KEY_CALLBACK:rim_to_me",
            "KEY_CALLBACK:rim_to_you",
            "KEY_CALLBACK:massage_to_me",
            "KEY_CALLBACK:massage_to_you",
            "KEY_CALLBACK:for_pay_offer",
            "KEY_CALLBACK:for_pay_looking",
            "KEY_CALLBACK:fetishes",
            "KEY_CALLBACK:virt",
            "KEY_CALLBACK:ready",

        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
