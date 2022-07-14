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

from ms_bot.dialogs.file_mgmt.file_loop_dialog import FileLoopDialog
from ms_bot.dialogs.file_mgmt.upload_dialog import UploadDialog
from settings.logger import CustomLogger
from helpers.copyright import USER_FILES_KB, BOT_MESSAGES


from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class MyFileDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(MyFileDialog, self).__init__(dialog_id or MyFileDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, MyFileDialog.answer_prompt_validator)
        )
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(FileLoopDialog(user_state, FileLoopDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainMyPhotoDialog",
                [
                    self.show_menu_step,
                    self.parse_choice_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMyPhotoDialog"

    async def show_menu_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_menu_step %s", MyFileDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(USER_FILES_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES["reprompt"]),
            ),
        )

    async def parse_choice_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_choice_step %s", MyFileDialog.__name__)
        try:
            chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        except Exception:
            chat_id = None
        try:
            message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        except Exception:
            message_id = None
        try:
            await rm_tg_message(step_context.context, chat_id, message_id)
        except Exception as e:
            logger.warning('Something went wrong %s', e)

        found_choice = step_context.result

        if found_choice == "KEY_CALLBACK:upload":
            return await step_context.begin_dialog(UploadDialog.__name__)
        elif found_choice == "KEY_CALLBACK:access":
            return await step_context.begin_dialog(FileLoopDialog.__name__)
        elif found_choice == "KEY_CALLBACK:back":
            return await step_context.end_dialog("need_replace_parent")
        else:
            return await step_context.replace_dialog(MyFileDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:upload",
            "KEY_CALLBACK:access",
            "KEY_CALLBACK:back",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
