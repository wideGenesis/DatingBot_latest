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

from settings.logger import CustomLogger
from helpers.copyright import (
    LOOKING_FOR_KB,
    sex_buttons,
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

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("loop_step %s", CreateAdvGoalsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        files = user_data.files_dict
        file_number = user_data.file_number

        return await step_context.begin_dialog(CreateAdvGoalsDialog.__name__, item)

    async def post_loop_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("post_loop_step %s", CreateAdvGoalsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        files = user_data.files_dict
        length = len(files) - 1

        if user_data.file_number < length:
            user_data.file_number += 1
            return await step_context.replace_dialog(CreateAdvGoalsDialog.__name__)

        if user_data.file_number >= length:
            user_data.file_number = 0
            return await step_context.end_dialog('need_replace_parent')

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:profile_region",

        ]:
            condition = True
        else:
            condition = False
        # await prompt_context.context.delete_activity(prompt_context.context.activity.id)

        return prompt_context.recognized.succeeded and condition
