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

from setup.logger import CustomLogger
from ..lib.messages import MAIN_MENU_KB
from ..dialogs.auth_reload_dialog import AuthReloadDialog

from ..dialogs.adv_menu_dialog import AdvMenuDialog
from ..dialogs.my_photo_dialog import MyPhotoDialog
from ..dialogs.my_profile_dialog import MyProfileDialog
from ..dialogs.my_settings_dialog import MySettingsDialog

from ..helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class MenuDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(MenuDialog, self).__init__(dialog_id or MenuDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TextPrompt(TextPrompt.__name__, MenuDialog.answer_prompt_validator))
        self.add_dialog(MyProfileDialog(user_state, MyProfileDialog.__name__))
        self.add_dialog(MyPhotoDialog(user_state, MyPhotoDialog.__name__))
        self.add_dialog(AdvMenuDialog(user_state, AdvMenuDialog.__name__))
        self.add_dialog(MySettingsDialog(user_state, MySettingsDialog.__name__))
        self.add_dialog(AuthReloadDialog(user_state, AuthReloadDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "MainMenuDialog",
                [
                    self.reload_cache_step,
                    self.show_menu_step,
                    self.parse_choice_step,
                    self.loop_menu_step
                ]
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMenuDialog"

    async def reload_cache_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('reload_cache_step %s', MenuDialog.__name__)
        return await step_context.begin_dialog(AuthReloadDialog.__name__)

    async def show_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('show_menu_step %s', MenuDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(MAIN_MENU_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def parse_choice_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('parse_choice_step %s', MenuDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        # if found_choice == 'KEY_CALLBACK:Профіль':
        #     return await step_context.begin_dialog(MyProfileDialog.__name__)
        if found_choice == 'KEY_CALLBACK:Мої файли':
            return await step_context.begin_dialog(MyPhotoDialog.__name__)
        elif found_choice == 'KEY_CALLBACK:Мої оголошення':
            return await step_context.begin_dialog(AdvMenuDialog.__name__)
        elif found_choice == 'KEY_CALLBACK:Налаштування':
            return await step_context.begin_dialog(MySettingsDialog.__name__)
        else:
            await step_context.context.send_activity('buy')
            return await step_context.cancel_all_dialogs(True)

    async def loop_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('loop_menu_step %s', MenuDialog.__name__)

        result_from_previous_step = step_context.result
        if result_from_previous_step == 'need_replace_parent':
            return await step_context.replace_dialog(MenuDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            'KEY_CALLBACK:Профіль',
            'KEY_CALLBACK:Мої файли',
            'KEY_CALLBACK:Мої оголошення',
            'KEY_CALLBACK:Налаштування',
        ]:
            condition = True
        else:
            condition = False

        return (
                prompt_context.recognized.succeeded
                and condition
        )
