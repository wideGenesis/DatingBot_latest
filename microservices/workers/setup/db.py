import os
from contextlib import contextmanager
import mysql.connector
import MySQLdb

server = os.environ.get('MYSQL_HOST', 'ENV UNAVAILABLE')
port = os.environ.get('MYSQL_PORT', 3306)
database = os.environ.get('MYSQL_DATABASE', 'ENV UNAVAILABLE')
username = os.environ.get('MYSQL_USER', 'ENV UNAVAILABLE')
password = os.environ.get('MYSQL_PASSWORD', 'ENV UNAVAILABLE')

connection_string = config = {
    'user': username,
    'password': password,
    'host': server,
    'database': database,
    'raise_on_warnings': True
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': database,
        'HOST': server,
        'PORT': port,
        'USER': username,
        'PASSWORD': password,
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },
}


@contextmanager
def get_db_cursor(commit=True):
    conn = None
    try:
        conn = mysql.connector.connect(**connection_string)
        with conn:
            with conn.cursor() as cur:
                yield cur
                if commit:
                    conn.commit()
    finally:
        if conn:
            conn.close()

# @contextmanager
# def get_db_cursor(commit=True):
#     conn = None
#     try:
#         conn = MySQLdb.connect(
#             host=server,
#             port=port,
#             user=username,
#             passwd=password,
#             db=database
#         )
#         with conn:
#             with conn.cursor() as cur:
#                 yield cur
#                 if commit:
#                     conn.commit()
#     finally:
#         if conn:
#             try:
#                 conn.close()
#             except Exception as e:
#                 print('!!!!!!!', e)
