import datetime

from botbuilder.core import ConversationState, UserState, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult

from settings.logger import CustomLogger
from ms_bot.dialogs.main_menu_dialog import MenuDialog
from ms_bot.dialogs.utils_dialog import UtilsDialog
from ms_bot.dialogs.auth_dialog import AuthDialog
from ms_bot.dialogs.telegram_registration_dialog import TelegramRegistrationDialog
from ms_bot.bots_models.models import CustomerProfile

logger = CustomLogger.get_logger('bot')


class MainDialog(ComponentDialog):
    def __init__(
            self,
            conversation_state: ConversationState,
            user_state: UserState,
            telemetry_client: BotTelemetryClient = None,

    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()

        # Add state property accessors
        self.user_profile_accessor = user_state.create_property("CustomerProfile")

        self.add_dialog(AuthDialog(user_state, AuthDialog.__name__))
        self.add_dialog(MenuDialog(user_state, MenuDialog.__name__))
        self.add_dialog(TelegramRegistrationDialog(user_state, TelegramRegistrationDialog.__name__))
        self.add_dialog(UtilsDialog(conversation_state, user_state, UtilsDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [
                    self.detect_channel_step,
                    self.is_auth_step,
                    self.routing_step,
                    self.menu_step,

                ]
            )
        )
        MainDialog.telemetry_client = self.telemetry_client
        AuthDialog.telemetry_client = self.telemetry_client
        TelegramRegistrationDialog.telemetry_client = self.telemetry_client
        UtilsDialog.telemetry_client = self.telemetry_client

        self.initial_dialog_id = "MainDialog"
        self.conversation_state = conversation_state
        self.user_state = user_state

    async def detect_channel_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('detect_channel_step %s', MainDialog.__name__)
        if step_context.context.activity.channel_id != 'telegram':
            await step_context.context.send_activity('Channel not supported')
            return await step_context.end_dialog()
        return await step_context.next([])

    async def is_auth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('is_auth_step %s', MainDialog.__name__)
        return await step_context.begin_dialog(AuthDialog.__name__)

    async def routing_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('routing_step %s', MainDialog.__name__)
        member_id = int(step_context.context.activity.from_property.id)

        if step_context.result is True:
            logger.debug('Routing %s to menu', member_id)
            return await step_context.next(step_context.result)

        if not step_context.result:
            logger.info('Not authorised! Routing %s to TelegramRegistrationDialog', member_id)
            return await step_context.begin_dialog(TelegramRegistrationDialog.__name__)

    async def menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        logger.debug('routing_step %s', MainDialog.__name__)
        user_data: CustomerProfile = await self.user_profile_accessor.get(step_context.context, CustomerProfile)
        user_data.updated_at = datetime.datetime.utcnow()
        member_id = int(step_context.context.activity.from_property.id)
        income_message = str(step_context.context.activity.text).strip().lower()

        if 'utils' in income_message and member_id in ['1887695430']:
            return await step_context.replace_dialog(UtilsDialog.__name__)

        return await step_context.begin_dialog(MenuDialog.__name__)


