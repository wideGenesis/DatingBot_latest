from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    UserState,
)

from settings.conf import AZURE_STORAGE_CONF, AZURE_BOT_CONF
from botbuilder.azure import BlobStorage, BlobStorageSettings

from ms_bot.adapter.adapter_with_error_handler import AdapterWithErrorHandler
from ms_bot.dialogs.main_dialog import MainDialog
from settings.logger import CustomLogger
from ms_bot.bots.dialog_bot import ConversationBot

logger = CustomLogger.get_logger('bot')


# Create adapter.
SETTINGS = BotFrameworkAdapterSettings(AZURE_BOT_CONF.BOT_APP_ID, AZURE_BOT_CONF.BOT_APP_PASSWORD)
BLOB_SETTINGS = BlobStorageSettings(
    connection_string=AZURE_STORAGE_CONF.STORAGE_CONNECTION_STRING,
    container_name=AZURE_STORAGE_CONF.BLOB_CONTAINER_NAME)

# Create MemoryStorage, UserState and ConversationState
MEMORY = BlobStorage(BLOB_SETTINGS)
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
# ADAPTER = BotFrameworkAdapter(SETTINGS)
ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

# LOOP = uvloop.new_event_loop()
# asyncio.set_event_loop(LOOP)  #TODO !!!

# Create telemetry client.
# Note the small 'client_queue_size'.  This is for demonstration purposes.  Larger queue sizes
# result in fewer calls to ApplicationInsights, improving bot performance at the expense of
# less frequent updates.
# INSTRUMENTATION_KEY = ms_bot_framework_config.DefaultConfig.APP_INSIGHTS_INSTRUMENTATION_KEY
# TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
#     INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=10
# )

# Code for enabling activity and personal information logging.
# TELEMETRY_LOGGER_MIDDLEWARE = TelemetryLoggerMiddleware(
#     telemetry_client=TELEMETRY_CLIENT,
#     log_personal_information=True
# )
# ADAPTER.use(TELEMETRY_LOGGER_MIDDLEWARE)

# Create dialogs and Bot
DIALOG = MainDialog(CONVERSATION_STATE, USER_STATE, telemetry_client=None)
BOT = ConversationBot(CONVERSATION_STATE, USER_STATE, DIALOG, None)

