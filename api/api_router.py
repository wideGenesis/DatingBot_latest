from typing import List

from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_crudrouter import OrmarCRUDRouter

import schemas
from crud.auth import AuthService
from db import models
from db.models import Area
from schemas import area
from fastapi import Request, Response, HTTPException, status, Depends
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_201_CREATED

from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


# https://fastapi-crudrouter.awtkns.com/

area_router = OrmarCRUDRouter(
    schema=models.Area,
    create_schema=area.BaseArea,
    update_schema=area.BaseArea,
    delete_all_route=False
)


@area_router.get('', response_model=List[area.Area])
async def get_all(
        credentials: HTTPBasicCredentials = Depends(security),
        auth_service: AuthService = Depends(),
):
    auth = await auth_service.authenticate_service(credentials)
    if auth:
        return await Area.objects.all()


redis_channel_router = OrmarCRUDRouter(
    schema=models.RedisChannel,
)
customer_router = OrmarCRUDRouter(
    schema=models.Customer,
)
advertisement_router = OrmarCRUDRouter(
    schema=models.Advertisement,
)
blacklist_router = OrmarCRUDRouter(
    schema=models.Blacklist,
)
