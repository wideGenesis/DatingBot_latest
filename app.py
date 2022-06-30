from core import api
import uvicorn

from settings.conf import FAST_API_CONF, DATABASE_CONF
from db.engine import DATABASE, ENGINE
from fastapi import FastAPI
from settings.logger import CustomLogger
from core.tables.models import METADATA
from startup_insert_fixture import fixture
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

logger = CustomLogger.get_logger('bot')

# TODO uncomment if tables creation needed, set SYNC Driver = export DB_DRIVER=postgresql
if DATABASE_CONF.DB_DRIVER == 'postgresql':
    METADATA.create_all(bind=ENGINE)

app = FastAPI(
    title='FastApi Microsoft Bot Framework',
    description='Microsoft Bot Implementation',
    version='1.0.0',
    openapi_tags=FAST_API_CONF.TAGS_META,
)

app.include_router(api.router)

app.state.database = DATABASE
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        logger.info(f'Connection to database {DATABASE.url.hostname} has been established')
        # await fixture()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        logger.info(f'Connection to database {DATABASE.url.hostname} has been closed')


if __name__ == '__main__':
    uvicorn.run('app:app', host=FAST_API_CONF.HOST, port=FAST_API_CONF.PORT, log_level='debug', reload=True)
