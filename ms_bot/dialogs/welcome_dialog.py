from botbuilder.core import UserState, BotTelemetryClient, NullTelemetryClient, MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog

from ..dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from setup.logger import CustomLogger
from ..helpers.hero_card_helper import welcome_hero_card

logger = CustomLogger.get_logger('bot')


class WelcomeDialog(ComponentDialog):

    def __init__(
            self,
            user_state: UserState,
            dialog_id: str = None,
            telemetry_client: BotTelemetryClient = NullTelemetryClient(),

    ):
        super(WelcomeDialog, self).__init__(dialog_id or WelcomeDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state

        self.add_dialog(TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WelcomeDialog",
                [
                    self.send_welcome_card,
                ]
            )
        )
        TelegramRegistrationDialog.telemetry_client = self.telemetry_client

        self.initial_dialog_id = "WelcomeDialog"
        self.customer_exists = None

    # async def user_exists_in_blob(self, step_context: WaterfallStepContext) -> DialogTurnResult:
    #     user_profile_accessor = self.user_state.create_property("EmployeeProfile")
    #     is_user_has_blob: EmployeeProfile = await user_profile_accessor.get(step_context.context, EmployeeProfile)
    #     if is_user_has_blob.city or is_user_has_blob.employeeId:
    #         return await step_context.end_dialog(self.customer_exists)
    #
    async def send_welcome_card(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('send_welcome_card %s', WelcomeDialog.__name__)
        welcome_message = MessageFactory.attachment(welcome_hero_card())

        await step_context.context.send_activity(welcome_message)

        return await step_context.end_dialog(True)
