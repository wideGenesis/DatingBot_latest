from botbuilder.core import UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
)

from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from settings.logger import CustomLogger

from core.tables.models import Customer

logger = CustomLogger.get_logger("bot")


class AuthDialog(ComponentDialog):
    def __init__(
        self,
        user_state: UserState,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(AuthDialog, self).__init__(dialog_id or AuthDialog.__name__)
        self.telemetry_client = telemetry_client
        self.user_state = user_state
        self.user_profile_accessor = self.user_state.create_property("CustomerProfile")

        self.add_dialog(
            TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__)
        )
        self.add_dialog(
            WaterfallDialog(
                "AuthDialog",
                [
                    # self.is_user_exists_in_blob,
                    self.is_user_exists_in_db,
                ],
            )
        )
        TelegramRegistrationDialog.telemetry_client = self.telemetry_client

        self.initial_dialog_id = "AuthDialog"
        self.customer_exists = None
        self.customer_instance = None

    async def is_user_exists_in_db(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        logger.debug("user_exists_in_db %s", AuthDialog.__name__)
        member_id = int(step_context.context.activity.from_property.id)
        # user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
        try:
            customer = await Customer.objects.get(member_id=member_id)
            self.customer_exists = True
            self.customer_instance = customer
            logger.debug("USER (%s) FOUND IN DB", member_id)

        except Exception:
            logger.warning("USER (%s) DOESN'T EXIST IN DB", member_id)
            self.customer_exists = None

        # if self.customer_exists is None:
        #     return await step_context.end_dialog(self.customer_exists)

        return await step_context.end_dialog(self.customer_exists)

