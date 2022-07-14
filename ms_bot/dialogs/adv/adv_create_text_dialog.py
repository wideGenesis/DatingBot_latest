from botbuilder.core import (
    MessageFactory,
    UserState,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    PromptValidatorContext,
    NumberPrompt,
)

from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, ChoicePrompt
from botbuilder.schema import Activity, ActivityTypes
import json

from helpers.constants import remove_last_message
from ms_bot.bots_models import CustomerProfile
from settings.logger import CustomLogger
from helpers.copyright import (
ADV_TEXT,
)


logger = CustomLogger.get_logger("bot")


class GetAdvTextDialog(ComponentDialog):
    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(GetAdvTextDialog, self).__init__(dialog_id or GetAdvTextDialog.__name__)

        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TextPrompt(TextPrompt.__name__)
        )
        self.add_dialog(
            WaterfallDialog(
                "GetAdvTextDialog",
                [
                    self.adv_text,
                    self.save_text,
                ],
            )
        )

        TextPrompt.telemetry_client = self.telemetry_client
        ChoicePrompt.telemetry_client = self.telemetry_client
        self.initial_dialog_id = "GetAdvTextDialog"

    async def adv_text(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("adv_text %s", GetAdvTextDialog.__name__)
        try:
            await remove_last_message(step_context, True)
        except KeyError:
            logger.warning('callback_query')
        except Exception:
            logger.exception('Something went wrong!')

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=Activity(
                    channel_data=json.dumps(ADV_TEXT),
                    type=ActivityTypes.message,
                ),
                retry_prompt=MessageFactory.text(
                    "Make your choice by clicking on the appropriate button above"
                ),
            ),
        )

    async def save_text(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug("save_text %s", GetAdvTextDialog.__name__)

        user_data: CustomerProfile = await self.user_profile_accessor.get(
            step_context.context, CustomerProfile
        )
        user_data.adv_text = str(step_context.result)
        return await step_context.end_dialog()
