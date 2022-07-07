from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
    Depends,
)
from fastapi.openapi.models import APIKey

from core.crud.advertisement import AdvertisementService
from core.services.api_service import ApiKeyService
from core.tables.models import Advertisement

router = APIRouter(
    prefix="/advertisement",
    tags=["Advertisement"],
)


@router.post(
    "/create/",
    response_model=Advertisement,
    response_model_exclude={"id", "created_at", "updated_at", "nickname"},
    status_code=status.HTTP_201_CREATED
)
async def create_adv(
        adv: Advertisement,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().create(adv)


@router.get("/list/",
            response_model=List[Advertisement],
            response_model_exclude={"id", "created_at", "updated_at", "customer"},
            status_code=status.HTTP_201_CREATED,
            )
async def list_adv(
        offset: int,
        limit: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().list(offset, limit)


@router.get("/get-advertisement-by/{area_id}",
            response_model=Advertisement,
            status_code=status.HTTP_201_CREATED
            )
async def get_by_area_id(
        area_id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_area(area_id)


@router.get("/get-advertisement-by/{redis_channel_id}",
            response_model=Advertisement,
            status_code=status.HTTP_201_CREATED
            )
async def get_by_redis_channel(
        redis_channel: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_redis_channel(redis_channel)


@router.get("/get-advertisement-by/{customer}",
            response_model=Advertisement,
            status_code=status.HTTP_201_CREATED
            )
async def get_by_publisher_id(
        customer: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_customer(customer)


@router.put("/update/",
            response_model=Advertisement,
            status_code=status.HTTP_201_CREATED
            )
async def create_adv(
        adv: Advertisement,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().update(adv)


@router.delete("/delete/",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_adv_by_id(
        _id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().delete(_id)
