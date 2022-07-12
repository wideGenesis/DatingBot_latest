import datetime
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

from core.tables.models import UserMediaFile
from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.file_management_dialog import FileManagementDialog

from settings.logger import CustomLogger
from helpers.copyright import BOT_MESSAGES
from ms_bot.dialogs.upload_dialog import UploadDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class FileLoopDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(FileLoopDialog, self).__init__(dialog_id or FileLoopDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(FileManagementDialog(user_state, FileManagementDialog.__name__))
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainFileLoopDialog",
                [
                    self.loop_step,
                    self.post_loop_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainFileLoopDialog"

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("loop_step %s", FileLoopDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        files = user_data.files_dict
        file_number = user_data.file_number
        print("file_number", file_number)

        if len(files) == 0:
            print('1111')
            await step_context.context.send_activity(BOT_MESSAGES["files_not_found"])
            return await step_context.end_dialog("need_replace_parent")

        item = files[file_number]
        print('file', item)
        return await step_context.begin_dialog(FileManagementDialog.__name__, item)

    async def post_loop_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("post_loop_step %s", FileLoopDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        files = user_data.files_dict
        length = len(files) - 1

        if user_data.file_number < length:
            user_data.file_number += 1
            return await step_context.replace_dialog(FileLoopDialog.__name__)

        if user_data.file_number >= length:
            user_data.file_number = 0
            await step_context.context.send_activity("Bye!")
            return await step_context.end_dialog(True)
