from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import contextmanager
from settings.conf import DatabaseConfig

DB = DatabaseConfig()

DB_URL: str = f"{DB.DB_DRIVER}://{DB.DB_USER}:{DB.DB_PASSWORD}@{DB.DB_HOST}:{DB.DB_PORT}/{DB.DB_NAME}"
METADATA = MetaData()
DATABASE = Database(DB_URL)

if DB.DB_DRIVER == 'postgresql+asyncpg':
    print('ASYNC', DB_URL)
    ENGINE = create_async_engine(DB_URL, future=True, echo=True)
    SESSION = sessionmaker(bind=ENGINE, expire_on_commit=False, class_=AsyncSession)

if DB.DB_DRIVER == 'postgresql':
    print('SYNC', DB_URL)
    ENGINE = create_engine(DB_URL)
    SESSION = sessionmaker(ENGINE)


BASE = declarative_base()


async def get_session() -> AsyncSession:
    async with SESSION() as session:
        yield session

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
