import api
import uvicorn

from config.conf import FAST_API_CONF, TAGS_META
from db.engine import DATABASE
from fastapi import FastAPI
from setup.logger import CustomLogger

logger = CustomLogger.get_logger('bot')


app = FastAPI(
    title='FastApi Microsoft Bot Framework',
    description='Microsoft Bot Implementation',
    version='1.0.0',
    openapi_tags=TAGS_META,
)

app.include_router(api.router)

app.state.database = DATABASE


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        logger.info(f'Connection to database {DATABASE.url.hostname} has been established')


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        logger.info(f'Connection to database {DATABASE.url.hostname} has been closed')


if __name__ == '__main__':
    uvicorn.run('app:app', host=FAST_API_CONF.HOST, port=FAST_API_CONF.PORT, log_level='debug', reload=True)
