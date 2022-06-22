import logging
import os
from typing import Optional, Union

from pydantic import BaseSettings

IS_LOCAL_ENV = int(os.environ.get('IS_LOCAL_ENV', 1))


class ProjectConfig(BaseSettings):
    # ########## Global logger settings ########## #
    LOG_TO: int = int(os.environ.get('LOG_TO', 0))
    if os.environ.get('LOGGER_LEVEL') == 'DEBUG':
        LOGGER_LEVEL: Union[int, str] = logging.DEBUG
        DJANGO_LOGGER_LEVEL = 'DEBUG'
    else:
        LOGGER_LEVEL: Union[int, str] = logging.INFO
        DJANGO_LOGGER_LEVEL = 'DEBUG'

    # ########## Global logger settings ########## #
    MAIL_PORT: Union[int, str] = os.environ.get('MAIL_PORT', '')
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', '')
    MAIL_USER: str = os.environ.get('MAIL_USER', '')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '')

    # ########## Database settings ########## #
    DB_HOST: str = os.environ.get('DB_HOST', '')
    DB_NAME: str = os.environ.get('DB_NAME', '')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD', '')
    DB_USER: str = os.environ.get('DB_USER', '')
    DB_PORT: str = os.environ.get('DB_PORT', '')

    DB_DRIVER: str = os.environ.get('DB_DRIVER', '')
    DB_URL: str = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # ########## Redis settings ########## #
    REDIS_MESSAGE_LIMIT: int = 1000
    REDIS_PORT: int = 6380
    REDIS_DB: str = os.environ.get('REDIS_DB', '')
    REDIS_APP_NAME: str = os.environ.get('REDIS_APP_NAME', '')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD', '')

    if IS_LOCAL_ENV == 1:
        REDIS_URI: str = f'redis://localhost:6379/{REDIS_DB}'

    else:
        # REDIS_URI = f'rediss://:{REDIS_PASSWORD}@{REDIS_APP_NAME}.redis.cache.windows.net:{REDIS_PORT}/{REDIS_DB}'
        REDIS_URI: str = f'redis://localhost:6379/{REDIS_DB}'

    # REDIS KEYS
    REDIS_ADMIN_MAIL_QUEUE_KEY: str = 'admin-mail-queue'
    REDIS_HEALTH_CHECK_KEY: str = 'health-check'

    # REDIS STREAM KEYS
    STREAM_NOTIFICATION_KEY = 'notifications'
    STREAM_INBOX_KEY = 'inbox'
    STREAM_EMAIL_KEY = 'email'
    STREAM_PRODUCER = 'bot-framework'

    # ########## GCP settings ########## #
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')


PROJECT_CONF = ProjectConfig()


class AzureConfig(BaseSettings):
    # ########## Azure Storage settings ########## #
    STORAGE_ACCOUNT_NAME: str = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', '')
    STORAGE_CONNECTION_STRING: str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
    STORAGE_KEY: str = os.environ.get('AZURE_STORAGE_KEY', '')
    BLOB_CONTAINER_NAME: str = 'bot'
    BLOB_CONTAINER_NAME_MEDIA: str = 'media'

    # ########## Azure ADFS settings ########## #
    AUTH_TENANT_ID: str = os.environ.get('AUTH_TENANT_ID', '')
    AUTH_CLIENT_ID: str = os.environ.get('AUTH_CLIENT_ID', '')
    AUTH_CLIENT_SECRET: str = os.environ.get('AUTH_CLIENT_SECRET', '')

    # ########## Azure Bot settings ########## #
    BOTAPPID: str = os.environ.get('BOTAPPID', '')
    BOTAPPPASSWORD: str = os.environ.get('BOTAPPPASSWORD', '')
    PORT: int = 3978
    MAINTENANCE: int = int(os.environ.get('MAINTENANCE', '0'))

    # ########## Azure App Insights settings ########## #
    APP_INSIGHTS_INSTRUMENTATION_KEY: str = os.environ.get('AppInsightsInstrumentationKey', '')


AZURE_CONF = AzureConfig()


class DjangoConfig(BaseSettings):
    # ########## Django settings ########## #
    DJANGO_SETTINGS_MODULE: str = 'mlnw.settings'
    DJANGO_ALLOWED_HOSTS: str = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
    ALLOWED_CIDR_NETS: str = os.environ.get('ALLOWED_CIDR_NETS', '')
    DJANGO_DEBUG: int = int(os.environ.get('DJANGO_DEBUG', 0))
    DJANGO_SECRET_KEY: str = os.environ.get('DJANGO_SECRET_KEY', '')
    DOMAIN: str = os.environ.get('DOMAIN', '')
    HTTP_X_FORWARDED_PROTO: str = 'https'
    HTTPS: str = 'on'
    TIMEZONE_DELAY: int = 0  # Summer +3/Winter+2


DJANGO_CONF = DjangoConfig()


class FastApiConfig(BaseSettings):
    # ########## FastApi settings ########## #
    HOST: str = 'localhost'
    # HOST: str = '127.0.0.1'
    PORT: int = 3978
    # PORT: int = 8000

    DB_URL: str = PROJECT_CONF.DB_URL

    JWT_SECRET: str = os.environ.get('JWT_SECRET', '')
    JWT_ALGO: str = 'HS256'
    JWT_EXPIRES_S: int = 3600


FAST_API_CONF = FastApiConfig()

TAGS_META = [
    {
        'name': 'Auth',
        'description': 'Авторизация и регистрация',
    },
    {
        'name': 'Customer',
        'description': 'Создание, редактирование, удаление и просмотр пользователей',
    },
    {
        'name': 'Advertisement',
        'description': 'Создание, редактирование, удаление и просмотр объявлений',
    },
    {
        'name': 'Bot messages exchange',
        'description': 'Bot messages exchange',
    },
    {
        'name': 'Bot notification exchange',
        'description': 'Bot notification exchange',
    },
]