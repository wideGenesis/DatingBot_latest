import json

from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient, UserState
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import ActivityTypes, Activity

from settings.logger import CustomLogger
from helpers.copyright import USER_FILES_KB
from ms_bot.dialogs.file_access_dialog import FileAccessDialog
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from ms_bot.dialogs.upload_dialog import UploadDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class MyPhotoDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(MyPhotoDialog, self).__init__(dialog_id or MyPhotoDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TextPrompt(TextPrompt.__name__, MyPhotoDialog.answer_prompt_validator))
        self.add_dialog(TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__))
        self.add_dialog(UploadDialog(user_state, UploadDialog.__name__))
        self.add_dialog(FileAccessDialog(user_state, FileAccessDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainMyPhotoDialog",
                [
                    self.show_menu_step,
                    self.parse_choice_step,
                    # self.back_to_parent
                ]
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMyPhotoDialog"

    async def show_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('show_menu_step %s', MyPhotoDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(USER_FILES_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def parse_choice_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('parse_choice_step %s', MyPhotoDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        if found_choice == 'KEY_CALLBACK:Завантажити файл':
            return await step_context.begin_dialog(UploadDialog.__name__)
        elif found_choice == 'KEY_CALLBACK:доступ':
            return await step_context.begin_dialog(FileAccessDialog.__name__)
        elif found_choice == 'KEY_CALLBACK:Назад':
            return await step_context.end_dialog('need_replace_parent')
        else:
            await step_context.context.send_activity('Bye!')
            return await step_context.cancel_all_dialogs(True)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            'KEY_CALLBACK:Завантажити файл',
            'KEY_CALLBACK:доступ',
            'KEY_CALLBACK:Видалити файл',
            'KEY_CALLBACK:Назад'
        ]:
            condition = True
        else:
            condition = False

        return (
                prompt_context.recognized.succeeded
                and condition
        )




