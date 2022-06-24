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
from ms_bot.bots_models.models import CustomerProfile

from settings.logger import CustomLogger
from helpers.copyright import profile_kb

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger('bot')


class MySettingsDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(MySettingsDialog, self).__init__(dialog_id or MySettingsDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(TextPrompt(TextPrompt.__name__, MySettingsDialog.answer_prompt_validator))
        self.add_dialog(
            WaterfallDialog(
                "MainMySettingsDialog",
                [
                    self.show_menu_step,
                    self.parse_choice_step,
                    # self.back_to_parent
                ]
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMySettingsDialog"

    async def show_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('show_menu_step %s', MySettingsDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)

        message = f'Мова бота: {user_data.lang}' \
                  f'Моя стать: {user_data.gender}' \
                  f'Мій вік: {user_data.age}' \
                  f'Переважний вік партнера: {user_data.prefer_age}' \
                  f'Я шукаю: {user_data.looking_gender}' \
                  f'Мета пошуків: {user_data.looking_for}' \
                  f'Моє місто: {user_data.area_id}' \
                  f'Мій телефон: {user_data.phone}'
        await step_context.context.send_activity(message)

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(profile_kb),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text('Зробіть вибір, натиснувши на відповідну кнопку вище'),
            )
        )

    async def parse_choice_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('parse_choice_step %s', MySettingsDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        if found_choice == 'KEY_CALLBACK:Редагувати профіль':
            return await step_context.begin_dialog()
        elif found_choice == 'KEY_CALLBACK:Назад':
            return await step_context.end_dialog(True)
        else:
            await step_context.context.send_activity('buy')
            return await step_context.cancel_all_dialogs(True)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            'KEY_CALLBACK:Редагувати профіль',
            'KEY_CALLBACK:Назад'
        ]:
            condition = True
        else:
            condition = False

        return (
                prompt_context.recognized.succeeded
                and condition
        )




