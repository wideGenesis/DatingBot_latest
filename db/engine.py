from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import contextmanager
from settings.conf import DATABASE_CONF


METADATA = MetaData()
DATABASE = Database(DATABASE_CONF.DB_URL)

if DATABASE_CONF.DB_DRIVER != 'postgresql':
    ENGINE = create_async_engine(DATABASE_CONF.DB_URL, future=True, echo=True)
    SESSION = sessionmaker(bind=ENGINE, expire_on_commit=False, class_=AsyncSession)
else:
    ENGINE = create_engine(DATABASE_CONF.DB_URL)
    SYNC_SESSION = sessionmaker(ENGINE)

BASE = declarative_base()


async def get_session() -> AsyncSession:
    async with SESSION() as session:
        yield session

# BASE.metadata.create_all(bind=ASYNC_ENGINE)


# @contextmanager
# async def get_async_db_cursor(commit=True, loop=None):
#     engine = await create_engine(user=username, db=database,
#                                  host=server, password=password, loop=loop)
#
#     async with engine.acquire() as conn:
#         with conn.cursor() as cur:
#             yield cur
#             if commit:
#                 conn.commit()
#
#     engine.close()
#     await engine.wait_closed()


# @contextmanager
# def get_sync_db_cursor(commit=True):
#     conn = None
#     try:
#         conn = DATABASE_CONF.CONNECTOR
#         with conn:
#             with conn.cursor() as cur:
#                 yield cur
#                 if commit:
#                     conn.commit()
#     finally:
#         if conn:
#             conn.close()
