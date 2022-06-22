import traceback

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState,
    TurnContext,
)

from ms_bot.lib.messages import BOT_MESSAGES
from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')


class AdapterWithErrorHandler(BotFrameworkAdapter):
    def __init__(
        self,
        settings: BotFrameworkAdapterSettings,
        conversation_state: ConversationState,
    ):
        super().__init__(settings)
        self._conversation_state = conversation_state

        # Catch-all for errors.
        async def on_error(context: TurnContext, error: Exception):
            """
            Catch-all for errors.
            This check writes out errors to console log
            NOTE: In production environment, you should consider logging this to Azure
            application insights.
            """
            _exceptions = traceback.format_exc()
            logger.warning('EXCEPTION: %s', _exceptions)

            # Send a message to the user
            await context.send_activity(BOT_MESSAGES['exceptions_occurs'])

            # Clear out state
            nonlocal self
            await self._conversation_state.delete(context)

        self.on_turn_error = on_error
