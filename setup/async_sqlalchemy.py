import os
from contextlib import contextmanager
from aiomysql.sa import create_engine


server = os.environ.get('MYSQL_HOST', 'ENV UNAVAILABLE')
port = os.environ.get('MYSQL_PORT', 3306)
database = os.environ.get('MYSQL_DATABASE', 'ENV UNAVAILABLE')
username = os.environ.get('MYSQL_USER', 'ENV UNAVAILABLE')
password = os.environ.get('MYSQL_PASSWORD', 'ENV UNAVAILABLE')


@contextmanager
async def get_async_db_cursor(commit=True, loop=None):
    engine = await create_engine(user=username, db=database,
                                 host=server, password=password, loop=loop)

    async with engine.acquire() as conn:
        with conn.cursor() as cur:
            yield cur
            if commit:
                conn.commit()

    engine.close()
    await engine.wait_closed()
