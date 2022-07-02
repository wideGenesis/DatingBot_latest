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
    DialogReason
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import ActivityTypes, Activity

from core.tables.models import UserMediaFile
from ms_bot.bots_models.models import CustomerProfile

from settings.logger import CustomLogger
from helpers.copyright import send_file_kb, BOT_MESSAGES
from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class FileManagementDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(FileManagementDialog, self).__init__(dialog_id or FileManagementDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, FileManagementDialog.answer_prompt_validator)
        )

        self.add_dialog(
            WaterfallDialog(
                "MainFileManagementDialog",
                [
                    self.show_file_step,
                    self.parse_choice_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainFileManagementDialog"
        self.file = None

    async def show_file_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_step %s", FileManagementDialog.__name__)
        member_id = str(step_context.context.activity.from_property.id)
        self.file = step_context.options

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(send_file_kb(member_id, self.file["file"], self.file["privacy_type"])),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES['reprompt']),
            ),
        )

    async def parse_choice_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_choice_step %s", FileManagementDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        pk = self.file.get("id")
        privacy_type = self.file.get("privacy_type")
        file = self.file.get("file")

        found_choice = step_context.result
        if found_choice == 'KEY_CALLBACK:back':
            return await step_context.end_dialog('need_replace_parent')

        elif found_choice == 'KEY_CALLBACK:file_open_hidden':
            get_file = await UserMediaFile.objects.get_or_none(id=pk)
            if get_file is None:
                return await step_context.end_dialog('continue_parent')
            logger.warning(
                "file: %s, privacy_type: %s, pk: %s",
                file,
                privacy_type,
                pk,
            )

            privacy_type = (1 if privacy_type == 0 else 0)
            logger.warning("privacy_type: %s", privacy_type)

            await get_file.update(privacy_type=privacy_type, updated_at=datetime.datetime.utcnow())
            return await step_context.next('continue_parent')

        elif found_choice == 'KEY_CALLBACK:file_rm':
            return await step_context.next('continue_parent')

        elif found_choice == 'KEY_CALLBACK:next':
            return await step_context.next('continue_parent')

        else:
            await step_context.context.send_activity("Bye!")
            return await step_context.cancel_all_dialogs(True)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:back",
            "KEY_CALLBACK:file_open_hidden",
            "KEY_CALLBACK:file_rm",
            "KEY_CALLBACK:next",
            "KEY_CALLBACK:menu",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition

    @staticmethod
    async def choice_route(
            step_context: WaterfallStepContext,
            found_choice,
            user_data: CustomerProfile,
            list_id: int,
    ) -> DialogTurnResult:
        try:
            item = user_data.files_dict[list_id]
            pk = item["id"]
        except Exception:
            return await step_context.end_dialog("need_replace_parent")

        if found_choice == "KEY_CALLBACK:file_open_hidden":
            try:
                user_media_files = UserMediaFile.objects.get(id=pk)
                logger.warning(
                    "Obj: %s, privacy_type: %s, pk: %s",
                    user_media_files,
                    user_media_files.privacy_type,
                    pk,
                )
                user_media_files.privacy_type = (
                    1 if user_media_files.privacy_type == 0 else 0
                )
                user_media_files.save()
            except Exception:
                logger.exception("Get Customer from bd error")
            user_data.last_seen = datetime.datetime.utcnow()
            user_data.files_dict.pop(list_id)
            return await step_context.next([])

        elif found_choice == "KEY_CALLBACK:file_rm":
            try:
                user_media_files = UserMediaFile.objects.get(id=pk)
                user_media_files.is_archived = 1
                user_media_files.save()
            except Exception:
                logger.exception("Get Customer from bd error")
            user_data.last_seen = datetime.datetime.utcnow()
            user_data.files_dict.pop(list_id)

            return await step_context.next([])

        elif found_choice == "KEY_CALLBACK:next":
            return await step_context.next([])

        elif found_choice == "KEY_CALLBACK:back":
            return await step_context.end_dialog("need_replace_parent")

        else:
            await step_context.context.send_activity("buy")
            return await step_context.cancel_all_dialogs(True)
