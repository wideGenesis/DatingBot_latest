import logging
import os
from typing import Optional, Union

from pydantic import BaseSettings

IS_LOCAL_ENV = int(os.environ.get('IS_LOCAL_ENV', 1))


class EmailConfig(BaseSettings):
    # ########## Global email settings ########## #
    MAIL_PORT: Union[int, str] = os.environ.get('MAIL_PORT', '')
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', '')
    MAIL_USER: str = os.environ.get('MAIL_USER', '')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '')


EMAIL_CONF = EmailConfig()


class DatabaseConfig(BaseSettings):
    # ########## Database settings ########## #
    DB_HOST: str = os.environ.get('DB_HOST', '')
    DB_NAME: str = os.environ.get('DB_NAME', '')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD', '')
    DB_USER: str = os.environ.get('DB_USER', '')
    DB_PORT: str = os.environ.get('DB_PORT', '')

    # DB_DRIVER = 'postgresql+asyncpg'
    DB_DRIVER = 'postgresql'
    # DB_DRIVER = 'asyncmy'
    # DB_DRIVER = 'mssql+pymssql'
    # DB_DRIVER = 'mssql+pyodbc'

    # if DB_DRIVER in ['postgresql+asyncpg', 'postgresql']:
    #     import psycopg2
    #
    #     DJANGO_DATABASES = {
    #         'default': {
    #             'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #             'NAME': DB_NAME,
    #             'HOST': DB_HOST,
    #             'PORT': DB_PORT,
    #             'USER': DB_USER,
    #             'PASSWORD': DB_PASSWORD,
    #         },
    #     }
    #     CONNECTION_STRING = config = {
    #         'user': DB_USER,
    #         'password': DB_PASSWORD,
    #         'host': DB_HOST,
    #         'database': DB_NAME,
    #     }
    #     CONNECTOR = psycopg2.connect(**CONNECTION_STRING)
    # else:
    #     import mysql.connector
    #
    #     DATABASES = {
    #         'default': {
    #             'ENGINE': 'django.db.backends.mysql',
    #             'NAME': DB_NAME,
    #             'HOST': DB_HOST,
    #             'PORT': DB_PORT,
    #             'USER': DB_USER,
    #             'PASSWORD': DB_PASSWORD,
    #             'OPTIONS': {
    #                 'init_command': 'SET default_storage_engine=INNODB',
    #             }
    #         },
    #     }
    #
    #     CONNECTION_STRING = config = {
    #         'user': DB_USER,
    #         'password': DB_PASSWORD,
    #         'host': DB_HOST,
    #         'database': DB_NAME,
    #         'raise_on_warnings': True
    #     }
    #     CONNECTOR = mysql.connector.connect(**CONNECTION_STRING)


DATABASE_CONF = DatabaseConfig()


class RedisConfig(BaseSettings):
    # ########## Redis settings ########## #
    REDIS_MESSAGE_LIMIT: int = 1000
    REDIS_DB: str = os.environ.get('REDIS_DB', '')
    REDIS_APP_NAME: str = os.environ.get('REDIS_APP_NAME', '')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD', '')

    # REDIS KEYS
    REDIS_ADMIN_MAIL_QUEUE_KEY: str = 'admin-mail-queue'
    REDIS_HEALTH_CHECK_KEY: str = 'health-check'

    # REDIS STREAM KEYS
    STREAM_NOTIFICATION_KEY: str = 'notifications'
    STREAM_INBOX_KEY: str = 'inbox'
    STREAM_EMAIL_KEY: str = 'email'
    STREAM_PRODUCER: str = 'bot-framework'

    def get_redis_uri(self, is_local_env=1):
        if is_local_env == 1:  # Local Env is active
            REDIS_URL: str = f'redis://localhost:6379/{self.REDIS_DB}'

        else:  # Prod Env is active
            REDIS_URL: str = f'rediss://:{self.REDIS_PASSWORD}' \
                             f'@{self.REDIS_APP_NAME}.redis.cache.windows.net:6380/{self.REDIS_DB}'

        return REDIS_URL


REDIS_CONF = RedisConfig()
REDIS_URI = REDIS_CONF.get_redis_uri()


class LoggerConfig(BaseSettings):
    # ########## Global logger settings ########## #
    LOG_TO: int = int(os.environ.get('LOG_TO', 0))
    if os.environ.get('LOGGER_LEVEL') == 'DEBUG':
        LOGGER_LEVEL: Union[int, str] = logging.DEBUG
        DJANGO_LOGGER_LEVEL = 'DEBUG'
    else:
        LOGGER_LEVEL: Union[int, str] = logging.INFO
        DJANGO_LOGGER_LEVEL = 'DEBUG'


LOGGER_CONF = LoggerConfig()


class AzureStorageConfig(BaseSettings):
    # ########## Azure Storage settings ########## #
    STORAGE_ACCOUNT_NAME: str = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', '')
    STORAGE_CONNECTION_STRING: str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
    STORAGE_KEY: str = os.environ.get('AZURE_STORAGE_KEY', '')
    BLOB_CONTAINER_NAME: str = 'bot'
    BLOB_CONTAINER_NAME_MEDIA: str = 'media'


AZURE_STORAGE_CONF = AzureStorageConfig()


class AzureAppConfig(BaseSettings):
    # ########## Azure App/ADFS settings ########## #
    AUTH_TENANT_ID: str = os.environ.get('AUTH_TENANT_ID', '')
    AUTH_CLIENT_ID: str = os.environ.get('AUTH_CLIENT_ID', '')
    AUTH_CLIENT_SECRET: str = os.environ.get('AUTH_CLIENT_SECRET', '')


AZURE_APP_CONF = AzureAppConfig()


class AzureBotConfig(BaseSettings):
    # ########## Azure Bot settings ########## #
    BOT_APP_ID: str = os.environ.get('BOT_APP_ID', '')
    BOT_APP_PASSWORD: str = os.environ.get('BOT_APP_PASSWORD', '')
    PORT: int = 3978
    MAINTENANCE: int = int(os.environ.get('MAINTENANCE', '0'))

    # ########## Azure App Insights settings ########## #
    APP_INSIGHTS_INSTRUMENTATION_KEY: str = os.environ.get('APP_INSIGHTS_INSTRUMENTAL_KEY', '')


AZURE_BOT_CONF = AzureBotConfig()


class DjangoConfig(BaseSettings):
    # ########## Django settings ########## #
    DJANGO_SETTINGS_MODULE: str = 'django.settings'
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
    PORT: int = 3978
    # HOST: str = '127.0.0.1'
    # PORT: int = 8000

    # DB_URL: str = DATABASE_CONF.DB_URL

    JWT_SECRET: str = os.environ.get('JWT_SECRET', '')
    JWT_ALGO: str = 'HS256'
    JWT_EXPIRES_S: int = 3600

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


FAST_API_CONF = FastApiConfig()


class RegionApiConfig(BaseSettings):
    REGION_API_URL = "https://rnd-nlp-geoapi.azurewebsites.net/api/geocode"
    REGION_API_TOKEN = "u49h7hlg46hal23h49u9uaj94n"


REGION_API_CONF = RegionApiConfig()


class GoogleApisConfig(BaseSettings):
    GOOGLE_API_KEY: str = os.environ.get('GOOGLE_API_KEY', '')


GOOGLE_CONF = GoogleApisConfig()
