from botbuilder.core import (
    BotTelemetryClient,
    NullTelemetryClient,
    UserState,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
)

from botbuilder.dialogs.prompts import TextPrompt, ChoicePrompt

from ms_bot.bots_models.models import CustomerProfile
from ms_bot.dialogs.adv.adv_list_management_dialog import AdvListManagementDialog
from settings.logger import CustomLogger
from helpers.copyright import BOT_MESSAGES


logger = CustomLogger.get_logger("bot")


class AdvListLoopDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(AdvListLoopDialog, self).__init__(dialog_id or AdvListLoopDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(AdvListManagementDialog(user_state, AdvListManagementDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "MainAdvListLoopDialog",
                [
                    self.loop_step,
                    self.post_loop_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainAdvListLoopDialog"

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("loop_step %s", AdvListLoopDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        search_prefer_age = user_data.search_prefer_age

        files = user_data.files_dict
        file_number = user_data.file_number
        print("file_number", file_number)

        if len(files) == 0:
            await step_context.context.send_activity(BOT_MESSAGES["files_not_found"])
            return await step_context.end_dialog("need_replace_parent")

        item = files[file_number]
        # print('file', item)
        return await step_context.begin_dialog(AdvListManagementDialog.__name__, item)

    async def post_loop_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("post_loop_step %s", AdvListLoopDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        files = user_data.files_dict
        length = len(files) - 1

        if user_data.file_number < length:
            user_data.file_number += 1
            return await step_context.replace_dialog(AdvListLoopDialog.__name__)

        if user_data.file_number >= length:
            user_data.file_number = 0
            return await step_context.end_dialog('need_replace_parent')
