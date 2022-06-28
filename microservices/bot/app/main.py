from fastapi import FastAPI
from core import api
from db.engine import DATABASE, ENGINE, METADATA

import uvicorn

tags_metadata = [
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
        'description': 'Bot api/messages exchange',
    },
    {
        'name': 'Bot notification',
        'description': 'Bot api/notification exchange',
    },
]

app = FastAPI(
    title='FastApi Microsoft Bot Framework',
    description='Microsoft Bot Implementation',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)

METADATA.create_all(ENGINE)
app.state.database = DATABASE


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8000, log_level='debug')
