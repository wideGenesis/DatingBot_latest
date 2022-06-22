from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config.conf import PROJECT_CONF

METADATA = MetaData()
DATABASE = Database(PROJECT_CONF.DB_URL)

if PROJECT_CONF.DB_DRIVER != 'postgresql':
    ENGINE = create_async_engine(PROJECT_CONF.DB_URL, future=True, echo=True)
    SESSION = sessionmaker(bind=ENGINE, expire_on_commit=False, class_=AsyncSession)
else:
    ENGINE = create_engine(PROJECT_CONF.DB_URL)
    SYNC_SESSION = sessionmaker(ENGINE)

BASE = declarative_base()


async def get_session() -> AsyncSession:
    async with SESSION() as session:
        yield session

# BASE.metadata.create_all(bind=ASYNC_ENGINE)
