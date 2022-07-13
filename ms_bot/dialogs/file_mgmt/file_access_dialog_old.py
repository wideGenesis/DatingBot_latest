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

from settings.logger import CustomLogger
from helpers.copyright import send_file_kb, SEND_MEDIA_KB, BOT_MESSAGES
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from ms_bot.dialogs.upload_dialog import UploadDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class FileAccessDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(FileAccessDialog, self).__init__(dialog_id or FileAccessDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, FileAccessDialog.answer_prompt_validator)
        )
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainFileAccessDialog",
                [
                    self.show_file_0_step,
                    self.parse_0_step,
                    self.show_file_1_step,
                    self.parse_1_step,
                    self.show_file_2_step,
                    self.parse_2_step,
                    self.show_file_3_step,
                    self.parse_3_step,
                    # self.back_to_parent
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainFileAccessDialog"

    async def show_file_0_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_0_step %s", FileAccessDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        return await self.yield_file_and_kb(step_context, user_data, step=0)

    async def parse_0_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_0_choice_step %s", FileAccessDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )

        found_choice = step_context.result
        return await self.choice_route(step_context, found_choice, user_data, 0)

    async def show_file_1_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_1_step %s", FileAccessDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await self.yield_file_and_kb(step_context, user_data, step=1)

    async def parse_1_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_1_step %s", FileAccessDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        # item = user_data.files_dict.get(1)  # TODO
        # pk = item['id']

        found_choice = step_context.result
        return await self.choice_route(step_context, found_choice, user_data, 1)

    async def show_file_2_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_2_step %s", FileAccessDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await self.yield_file_and_kb(step_context, user_data, step=2)

    async def parse_2_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_2_step %s", FileAccessDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        # item = user_data.files_dict.get(2)  # TODO
        # pk = item['id']

        found_choice = step_context.result
        return await self.choice_route(step_context, found_choice, user_data, 2)

    async def show_file_3_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_file_3_step %s", FileAccessDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        return await self.yield_file_and_kb(step_context, user_data, step=3)

    async def parse_3_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_3_step %s", FileAccessDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        # item = user_data.files_dict.get(3)  # TODO
        # pk = item['id']

        found_choice = step_context.result
        return await self.choice_route(step_context, found_choice, user_data, 3)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:file_open_hidden",
            "KEY_CALLBACK:file_rm",
            "KEY_CALLBACK:next",
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

    @staticmethod
    async def yield_file_and_kb(
        step_context: WaterfallStepContext, user_data: CustomerProfile, step=None
    ) -> DialogTurnResult:
        print("files", user_data.files_dict)

        user_files = user_data.files_dict

        if len(user_files) == 0:
            await step_context.context.send_activity("У вас немає завантажених файлів")
            return await step_context.end_dialog("need_replace_parent")

        activities = []
        member_id = str(step_context.context.activity.from_property.id)

        try:
            item = user_files[step]
            print("file", item)
        except Exception:
            return await step_context.end_dialog("need_replace_parent")

        activities.append(
            Activity(
                channel_data=json.dumps(
                    send_file_kb(member_id, item["file"], item["privacy_type"])
                ),
                type=ActivityTypes.message,
            )
        )

        await step_context.context.send_activities(activities)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(SEND_MEDIA_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES["reprompt"]),
            ),
        )
