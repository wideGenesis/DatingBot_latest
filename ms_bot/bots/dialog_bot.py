"""
https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-v4-state?view=azure-bot-service-4.0&tabs=python
"""

from botbuilder.core import ConversationState, UserState, TurnContext, ActivityHandler, BotTelemetryClient, \
    NullTelemetryClient
from botbuilder.dialogs import Dialog

from config.conf import AZURE_CONF
from ms_bot.lib.storage_blob_helper import rm_user_blobs
from ms_bot.helpers.dialog_helper import DialogHelper
from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')


class ConversationBot(ActivityHandler):
    """Main Teams dialog to welcome users implementation."""

    def __init__(
            self,
            conversation_state: ConversationState,
            user_state: UserState,
            dialog_state: Dialog,
            telemetry_client: BotTelemetryClient,

    ):
        # super(ConversationBot, self).__init__(
        #     conversation_state, user_state, dialog_state, telemetry_client
        # )
        self.telemetry_client = telemetry_client

        if conversation_state is None:
            raise Exception("[DialogBot]: Missing parameter. conversation_state is required")
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if dialog_state is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog_state
        # Add state property accessors
        self.user_profile_accessor = self.user_state.create_property("EmployeeProfile")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.

        try:
            await self.conversation_state.save_changes(turn_context)
        except Exception:
            logger.warning('self.conversation_state.save_changes')
        try:
            await self.user_state.save_changes(turn_context)
        except Exception:
            logger.warning('self.user_state.save_changes')

    async def on_message_activity(self, turn_context: TurnContext):
        # достаем в каждом сообщении состояния, чтобы можно было их использовать в контексте диалогов
        # await self.user_profile_accessor.get(turn_context, EmployeeProfile)
        if turn_context.activity.text == '/reset_cache':
            member_id = turn_context.activity.from_property.id
            rm_user_blobs(member_id)
            return

        if AZURE_CONF.MAINTENANCE:
            await turn_context.send_activity('⚠️ Сервіс тимчасово недоступний  \n \n🔄 Відбувається процес оновлення')
            return

        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """
        Gets the telemetry client for logging events.
        """
        return self._telemetry_client

    # pylint:disable=attribute-defined-outside-init
    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """
        Sets the telemetry client for logging events.
        """
        if value is None:
            self._telemetry_client = NullTelemetryClient()
        else:
            self._telemetry_client = value
