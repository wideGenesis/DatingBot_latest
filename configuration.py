import logging
import os

MAINTENANCE = int(os.environ.get('MAINTENANCE', '0'))
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

AZURE_BLOB_CONTAINER_NAME = 'bot'
AZURE_BLOB_CONTAINER_NAME_MEDIA = 'media'
AZURE_STORAGE_HOST = 'azureblobmlnw'
AZURE_STORAGE_BLOB_DATA_EXPIRE = '00:01:00'

MS_BOT_PORT = 3978
APP_INSIGHTS_INSTRUMENTATION_KEY = os.environ.get('AppInsightsInstrumentationKey', '')


DJANGO_SETTINGS_MODULE = 'mlnw.settings'


REGION_API_URL = "https://rnd-nlp-geoapi.azurewebsites.net/api/geocode"
REGION_API_TOKEN = "u49h7hlg46hal23h49u9uaj94n"


HTTP_X_FORWARDED_PROTO = 'https'
HTTPS = 'on'

LOG_TO = int(os.environ.get('LOG_TO', 0))
if os.environ.get('LOGGER_LEVEL') == 'DEBUG':
    LOGGER_LEVEL = logging.DEBUG
    DJANGO_LOGGER_LEVEL = 'DEBUG'

else:
    LOGGER_LEVEL = logging.INFO
    DJANGO_LOGGER_LEVEL = 'DEBUG'


MAIL_FROM = 'svc-MAIL-onboarding@metinvestholding.com'
MAIL_SERVER = 'smtp.office365.com'


REDIS_MESSAGE_LIMIT = 1000
REDIS_PORT = 6380

#  Летнее+3/зимнее+2 время, поправка на тайм-зону
TIMEZONE_DELAY = 0

# Общее для всех с секретом
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')

# Разное для всех
MYSQL_HOST = os.environ.get('MYSQL_HOST', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', '')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_USER = os.environ.get('MYSQL_USER', '')
MYSQL_PORT = 3306

AZURE_STORAGE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', '')
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
AZURE_STORAGE_KEY = os.environ.get('AZURE_STORAGE_KEY', '')
DJANGO_ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_CIDR_NETS = os.environ.get('ALLOWED_CIDR_NETS', '')
DJANGO_DEBUG = int(os.environ.get('DJANGO_DEBUG', 0))
DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
DOMAIN = os.environ.get('DOMAIN', '')
IS_LOCAL_ENV = int(os.environ.get('IS_LOCAL_ENV', 1))

MICROSOFT_AUTH_TENANT_ID = 'b0bbbc89-2041-434f-8618-bc081a1a01d4'
MICROSOFT_AUTH_CLIENT_ID = os.environ.get('MICROSOFT_AUTH_CLIENT_ID', '')
MICROSOFT_AUTH_CLIENT_SECRET = os.environ.get('MICROSOFT_AUTH_CLIENT_SECRET', '')

MicrosoftAppId = os.environ.get('MicrosoftAppId', '')
MicrosoftAppPassword = os.environ.get('MicrosoftAppPassword', '')


REDIS_DB = os.environ.get('REDIS_DB', '')
REDIS_APP_NAME = os.environ.get('REDIS_APP_NAME', '')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

if IS_LOCAL_ENV == 1:
    REDIS_URI = f'redis://localhost:6379/{REDIS_DB}'

else:
    # REDIS_URI = f'rediss://:{REDIS_PASSWORD}@{REDIS_APP_NAME}.redis.cache.windows.net:{REDIS_PORT}/{REDIS_DB}'
    REDIS_URI = f'redis://localhost:6379/{REDIS_DB}'


# REDIS KEYS
REDIS_ADMIN_MAIL_QUEUE_KEY = 'admin-mail-queue'
REDIS_HEALTH_CHECK_KEY = 'health-check'

# REDIS STREAM KEYS
STREAM_NOTIFICATION_KEY = 'notifications'
STREAM_INBOX_KEY = 'inbox'
STREAM_EMAIL_KEY = 'email'
STREAM_PRODUCER = 'bot-framework'
