import os
from contextlib import contextmanager

DB_BACKEND = int(os.environ.get('DB_BACKEND', 'ENV UNAVAILABLE'))  # 0 - postgresql, 1 - mysql

if DB_BACKEND == 0:
    import psycopg2

    host = os.environ.get('POSTGRES_HOST', 'ENV UNAVAILABLE')
    database = os.environ.get('POSTGRES_DB', 'ENV UNAVAILABLE')
    user = os.environ.get('POSTGRES_USER', 'ENV UNAVAILABLE')
    password = os.environ.get('POSTGRES_PASSWORD', 'ENV UNAVAILABLE')
    port = os.environ.get('POSTGRES_PORT', '5432')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': database,
            'HOST': host,
            'PORT': port,
            'USER': user,
            'PASSWORD': password,
        },
    }
    CONNECTION_STRING = config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database,
    }
    CONNECTOR = psycopg2.connect(**CONNECTION_STRING)


else:
    import mysql.connector

    host = os.environ.get('POSTGRES_HOST', 'ENV UNAVAILABLE')
    database = os.environ.get('POSTGRES_DB', 'ENV UNAVAILABLE')
    user = os.environ.get('POSTGRES_USER', 'ENV UNAVAILABLE')
    password = os.environ.get('POSTGRES_PASSWORD', 'ENV UNAVAILABLE')
    port = int(os.environ.get('POSTGRES_PORT', 3306))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': database,
            'HOST': host,
            'PORT': port,
            'USER': user,
            'PASSWORD': password,
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=INNODB',
            }
        },
    }

    CONNECTION_STRING = config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database,
        'raise_on_warnings': True
    }

    CONNECTOR = mysql.connector.connect(**CONNECTION_STRING)


@contextmanager
def get_db_cursor(commit=True):
    conn = None
    try:
        conn = CONNECTOR
        with conn:
            with conn.cursor() as cur:
                yield cur
                if commit:
                    conn.commit()
    finally:
        if conn:
            conn.close()
