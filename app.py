import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from core import api
from db.engine import DATABASE
from fake_fixtures import db_fill_customer
from settings.conf import FAST_API_CONF, IS_LOCAL_ENV
from settings.logger import CustomLogger
from db.fixtures.startup_insert_fixture import fixture

logger = CustomLogger.get_logger("bot")

app = FastAPI(
    title="FastApi Microsoft Bot Framework",
    description="Microsoft Bot Implementation",
    version="1.0.0",
    openapi_tags=FAST_API_CONF.TAGS_META,
    redoc_url=None
)

origins = [  # TODO Add valid origins on prod
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://localhost",
    "http://localhost:8080"
    "http://mysite.localtest.me:3978/"
    "https://mysite.localtest.me:3978/",
    "https://mysite.localtest.me:8000/",
    "https://mysite.localtest.me:8000/",
    "http://mysite.localtest.me:8080/",
    "https://mysite.localtest.me:8080/",
]
# if IS_LOCAL_ENV == 0:
#     app.add_middleware(HTTPSRedirectMiddleware)  # TODO Uncomment on prod
#     app.add_middleware(
#         TrustedHostMiddleware, allowed_hosts=[
#             "localhost",
#             "127.0.0.1",
#             "https://fast-love.azurewebsites.net/",
#             "fast-love.azurewebsites.net/",
#             "*.azurewebsites.net/",
#         ]
#     )
#     app.add_middleware(GZipMiddleware, minimum_size=1000)
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )


app.include_router(api.router)

app.state.database = DATABASE
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        logger.info(
            f"Connection to database {DATABASE.url.hostname} has been established"
        )
        # await fixture()  # TODO Uncomment when need a fill DB
        # await db_fill_customer(50)


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        logger.info(f"Connection to database {DATABASE.url.hostname} has been closed")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=FAST_API_CONF.HOST,
        port=FAST_API_CONF.PORT,
        log_level="debug",
        reload=True,
    )
