import traceback
import uuid

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter, MemoryStorage, UserState, ConversationState,

)

import ms_bot_framework_config
from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')

name = "ms_botfw"
appConfig = ms_bot_framework_config.DefaultConfig
# connection_name = ms_bot_framework_config.DefaultConfig.CONNECTION_NAME
SETTINGS = BotFrameworkAdapterSettings(
    appConfig.APP_ID,
    appConfig.APP_PASSWORD)
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



