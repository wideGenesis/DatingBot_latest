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
from helpers.copyright import send_file_kb, SEND_MEDIA_KB
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
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

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, FileLoopDialog.answer_prompt_validator)
        )
        self.add_dialog(
            TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__)
        )
        self.add_dialog(
            FileManagementDialog(user_state, FileManagementDialog.__name__)
        )
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainFileLoopDialog",
                [
                    self.show_file_step,
                    self.back_to_parent
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainFileLoopDialog"
        self.user_files_list = None

    async def show_file_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_step %s", FileLoopDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        self.user_files_list = user_data.files_dict
        for item in self.user_files_list:
            await step_context.begin_dialog(FileManagementDialog.__name__, item)
        
        return await step_context.next([])

    async def back_to_parent(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("back_to_parent from %s", FileLoopDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await step_context.end_dialog(user_data)

   
