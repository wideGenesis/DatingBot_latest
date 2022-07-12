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
from ms_bot.bots_models.models import CustomerProfile
from settings.logger import CustomLogger
from helpers.copyright import (
    profile_kb,
    LANG_CHOICE,
    SEX_CHOICE,
    BOT_MESSAGES,
)
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


class MyProfileDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(MyProfileDialog, self).__init__(dialog_id or MyProfileDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, MyProfileDialog.answer_prompt_validator)
        )
        self.add_dialog(
            TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__)
        )
        self.add_dialog(
            WaterfallDialog(
                "MainMyProfileDialog",
                [
                    self.show_menu_step,
                    self.parse_choice_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMyProfileDialog"

    async def show_menu_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_menu_step %s", MyProfileDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        member_id = int(step_context.context.activity.from_property.id)

        message = (  # TODO Internalize
            f"Мова бота: {LANG_CHOICE[user_data.lang]}  \n \n"
            f"Моя стать: {SEX_CHOICE[int(user_data.self_sex)]}  \n \n"
            f"Мій вік: {user_data.age}  \n \n"
            f"Мій телефон: {user_data.phone} (прихований від усіх)  \n \n"
            f"Мій email: {user_data.email} (прихований від усіх)  \n \n"
            f"Мій telegram: {user_data.nickname} (прихований від усіх)  \n \n"
            f"HIV Status (прихований від усіх): {user_data.hiv_status}  \n \n" 
            f"Алкоголь: {user_data.alco_status}  \n \n"
            f"Наркотики: {user_data.drugs_status}  \n \n"
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(profile_kb(message)),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(BOT_MESSAGES["reprompt"]),
            ),
        )

    async def parse_choice_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_choice_step %s", MyProfileDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        if found_choice == "KEY_CALLBACK:edit_profile":
            return await step_context.begin_dialog(TelegramRegistrationDialog.__name__)
        elif found_choice == "KEY_CALLBACK:back":
            return await step_context.end_dialog("need_replace_parent")
        else:
            return await step_context.end_dialog("need_replace_parent")

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:edit_profile",
            "KEY_CALLBACK:back"
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
