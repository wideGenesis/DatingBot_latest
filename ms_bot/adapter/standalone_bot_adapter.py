import traceback
import uuid

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter, MemoryStorage, UserState, ConversationState,

)

from config.conf import AZURE_CONF
from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')

SETTINGS = BotFrameworkAdapterSettings(
    AZURE_CONF.BOTAPPID,
    AZURE_CONF.BOTAPPPASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
memory = MemoryStorage()
user_state = UserState(memory)
conversation_state = ConversationState(memory)


async def on_error(context: TurnContext, error: Exception):
    _exceptions = traceback.format_exc()
    logger.debug('ERROR: %s', error)
    logger.debug('EXCEPTION: %s', _exceptions)

    await conversation_state.delete(context)

APP_ID = SETTINGS.app_id if SETTINGS.app_id else uuid.uuid4()
# ADAPTER.on_turn_error = on_error



