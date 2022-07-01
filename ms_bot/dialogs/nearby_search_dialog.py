import json

from botbuilder.core import (
    MessageFactory,
    BotTelemetryClient,
    NullTelemetryClient,
    UserState,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import ActivityTypes, Activity

from ms_bot.dialogs.my_photo_dialog import MyPhotoDialog
from ms_bot.dialogs.my_profile_dialog import MyProfileDialog
from settings.logger import CustomLogger
from helpers.copyright import MAIN_MENU_KB

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class NearbySearchDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(NearbySearchDialog, self).__init__(
            dialog_id or NearbySearchDialog.__name__
        )
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, NearbySearchDialog.answer_prompt_validator)
        )
        self.add_dialog(
            WaterfallDialog(
                "MainNearbySearchDialog",
                [
                    self.show_nearby_people_step,
                    self.parse_choice_step,
                    self.loop_menu_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainNearbySearchDialog"

    async def show_nearby_people_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_menu_step %s", NearbySearchDialog.__name__)

    async def parse_choice_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_choice_step %s", NearbySearchDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

    async def loop_menu_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("loop_menu_step %s", NearbySearchDialog.__name__)

        result_from_previous_step = step_context.result
        if result_from_previous_step == "need_replace_parent":
            return await step_context.replace_dialog(NearbySearchDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:nearby_people",
            "KEY_CALLBACK:adv_search",
            "KEY_CALLBACK:my_profile",
            "KEY_CALLBACK:files",
            "KEY_CALLBACK:settings",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
