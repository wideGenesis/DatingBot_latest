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
    "/create", response_model=Advertisement, status_code=status.HTTP_201_CREATED
)
async def create_adv(
    adv: Advertisement, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().create(adv)


@router.get("/list", response_model=List[Advertisement])
async def get_adv_list(
    offset: int, limit: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().list(offset, limit)


@router.get("/advertisement/{area_id}", response_model=Advertisement)
async def get_by_area_id(
    area_id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_area(area_id)


@router.get("/advertisement/{redis_channel_id}", response_model=Advertisement)
async def get_by_redis_channel(
    redis_channel: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_redis_channel(redis_channel)


@router.get("/advertisement/{publisher_id}", response_model=Advertisement)
async def get_by_publisher_id(
    publisher_id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().get_by_publisher_id(publisher_id)


@router.put("/update", response_model=Advertisement)
async def create_adv(
    adv: Advertisement, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await AdvertisementService().update(adv)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adv_by_id(
    _id: int, api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    await AdvertisementService().delete(_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.get('/', response_model=List[schemas.Advertisement])
# def get_advertisements(
#         user: schemas.User = Depends(get_current_user),
#         advertisement_service: AdvertisementService = Depends(),
# ):
#     return advertisement_service.get_many(user.id)
#
#
# @router.post('/', response_model=schemas.Advertisement, status_code=status.HTTP_201_CREATED)
# def create_advertisement(
#         advertisement_data: schemas.AdvertisementCreate,
#         user: schemas.User = Depends(get_current_user),
#         advertisement_service: AdvertisementService = Depends(),
# ):
#     return advertisement_service.create(user.id, advertisement_data)
#
#
# @router.get('/{advertisement_id}', response_model=schemas.Advertisement)
# def get_advertisement(
#         advertisement_id: int,
#         user: schemas.User = Depends(get_current_user),
#         advertisement_service: AdvertisementService = Depends(),
# ):
#     return advertisement_service.get(user.id, advertisement_id)
#
#
# @router.put('/{advertisement_id}', response_model=schemas.Advertisement)
# def update_advertisement(
#         advertisement_id: int,
#         advertisement_data: schemas.AdvertisementUpdate,
#         user: schemas.User = Depends(get_current_user),
#         advertisement_service: AdvertisementService = Depends(),
# ):
#     return advertisement_service.update(user.id, advertisement_id, advertisement_data)
#
#
# @router.delete('/{advertisement_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_advertisement(
#         advertisement_id: int,
#         user: schemas.User = Depends(get_current_user),
#         advertisement_service: AdvertisementService = Depends(),
# ):
#     advertisement_service.delete(user.id, advertisement_id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
