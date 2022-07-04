import json
import pickle

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

from ms_bot.bots_models import CustomerProfile
from settings.logger import CustomLogger
from helpers.copyright import MAIN_MENU_KB, BOT_MESSAGES
from ms_bot.dialogs.reload_cache_dialog import ReloadCacheDialog

from ms_bot.dialogs.adv_menu_dialog import AdvMenuDialog
from ms_bot.dialogs.my_file_dialog import MyFileDialog
from ms_bot.dialogs.my_profile_dialog import MyProfileDialog
from ms_bot.dialogs.nearby_search_dialog import NearbySearchDialog

from ms_bot.bot_helpers.telegram_helper import rm_tg_message

logger = CustomLogger.get_logger("bot")


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

        self.add_dialog(
            TextPrompt(TextPrompt.__name__, MenuDialog.answer_prompt_validator)
        )
        self.add_dialog(MyProfileDialog(user_state, MyProfileDialog.__name__))
        self.add_dialog(MyFileDialog(user_state, MyFileDialog.__name__))
        self.add_dialog(AdvMenuDialog(user_state, AdvMenuDialog.__name__))
        self.add_dialog(ReloadCacheDialog(user_state, ReloadCacheDialog.__name__))
        self.add_dialog(NearbySearchDialog(user_state, NearbySearchDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "MainMenuDialog",
                [
                    self.reload_cache_step,
                    self.show_menu_step,
                    self.parse_choice_step,
                    self.loop_menu_step,
                ],
            )
        )
        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "MainMenuDialog"

    async def reload_cache_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("reload_cache_step %s", MenuDialog.__name__)
        return await step_context.begin_dialog(ReloadCacheDialog.__name__)

    async def show_menu_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("show_menu_step %s", MenuDialog.__name__)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(MAIN_MENU_KB),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    BOT_MESSAGES['reprompt']
                ),
            ),
        )

    async def parse_choice_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("parse_choice_step %s", MenuDialog.__name__)
        chat_id = f"{step_context.context.activity.channel_data['callback_query']['message']['chat']['id']}"
        message_id = f"{step_context.context.activity.channel_data['callback_query']['message']['message_id']}"
        await rm_tg_message(step_context.context, chat_id, message_id)

        found_choice = step_context.result

        if found_choice == "KEY_CALLBACK:nearby_people":
            return await step_context.begin_dialog(NearbySearchDialog.__name__)

        elif found_choice == "KEY_CALLBACK:adv_search":
            return await step_context.begin_dialog(AdvMenuDialog.__name__)

        elif found_choice == "KEY_CALLBACK:my_profile":
            return await step_context.begin_dialog(MyProfileDialog.__name__)

        elif found_choice == "KEY_CALLBACK:files":
            return await step_context.begin_dialog(MyFileDialog.__name__)

        elif found_choice == "KEY_CALLBACK:scrape":
            await step_context.context.send_activity('Not implemented')
            return await step_context.replace_dialog(MenuDialog.__name__)

        else:
            await step_context.context.send_activity("bye!")
            return await step_context.cancel_all_dialogs(True)

    async def loop_menu_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("loop_menu_step %s", MenuDialog.__name__)

        result_from_previous_step = step_context.result
        if result_from_previous_step == "need_replace_parent":
            print('>>>>>>>>>>>>', result_from_previous_step)

            return await step_context.replace_dialog(MenuDialog.__name__)
        else:
            res: CustomerProfile = result_from_previous_step
            print('<<<<<>>>>>>>>>>>>>>>>>', res.pk)
            return await step_context.replace_dialog(MenuDialog.__name__)

    @staticmethod
    async def answer_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        _value = prompt_context.context.activity.text

        if _value in [
            "KEY_CALLBACK:nearby_people",
            "KEY_CALLBACK:adv_search",
            "KEY_CALLBACK:my_profile",
            "KEY_CALLBACK:files",
            "KEY_CALLBACK:settings",
            "KEY_CALLBACK: scrape",
        ]:
            condition = True
        else:
            condition = False

        return prompt_context.recognized.succeeded and condition
