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
from helpers.copyright import ADV_MENU_KB
from ms_bot.dialogs.reload_cache_dialog import ReloadCacheDialog

from ms_bot.dialogs.adv_show_dialog import MyAdvDialog
from ms_bot.dialogs.adv_create_dialog import CreateAdvDialog
from ms_bot.dialogs.my_photo_dialog import MyPhotoDialog
from ms_bot.dialogs.my_profile_dialog import MyProfileDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class AdvMenuDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(AdvMenuDialog, self).__init__(dialog_id or AdvMenuDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TextPrompt(TextPrompt.__name__, AdvMenuDialog.answer_prompt_validator))
        self.add_dialog(MyProfileDialog(user_state, MyProfileDialog.__name__))
        self.add_dialog(MyPhotoDialog(user_state, MyPhotoDialog.__name__))
        self.add_dialog(CreateAdvDialog(user_state, CreateAdvDialog.__name__))
        self.add_dialog(MyAdvDialog(user_state, MyAdvDialog.__name__))
        self.add_dialog(ReloadCacheDialog(user_state, ReloadCacheDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "MainAdvMenuDialog",
                [
                    self.show_menu_step,
                    self.parse_choice_step,
                    self.loop_menu_step
                ]
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainAdvMenuDialog"

    async def show_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('show_menu_step %s', AdvMenuDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(ADV_MENU_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def parse_choice_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('parse_choice_step %s', AdvMenuDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        if found_choice == 'KEY_CALLBACK:create_adv':
            return await step_context.begin_dialog(CreateAdvDialog.__name__)
        elif found_choice == 'KEY_CALLBACK:income_adv':
            # return await step_context.begin_dialog(MyAdvDialog.__name__)
            pass
        elif found_choice == 'KEY_CALLBACK:review_adv':
            # return await step_context.begin_dialog(MyAdvDialog.__name__)
            pass
        elif found_choice == 'KEY_CALLBACK:back':
            return await step_context.end_dialog()

        else:
            await step_context.context.send_activity('buy')
            return await step_context.cancel_all_dialogs(True)

    async def loop_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('loop_menu_step %s', AdvMenuDialog.__name__)

        result_from_previous_step = step_context.result
        if result_from_previous_step == 'need_replace_parent':
            return await step_context.replace_dialog(AdvMenuDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            'KEY_CALLBACK:income_adv',
            'KEY_CALLBACK:review_adv',
            'KEY_CALLBACK:create_adv',
            'KEY_CALLBACK:back',
        ]:
            condition = True
        else:
            condition = False

        return (
                prompt_context.recognized.succeeded
                and condition
        )
