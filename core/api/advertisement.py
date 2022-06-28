from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from core.schemas.advertisement import AdvertisementExpose
from core.crud.advertisement import AdvertisementService
from core.schemas.customer import CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix='/advertisement',
    tags=['Advertisement'],
)


@router.post('/create', response_model=AdvertisementExpose, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate):
    return await AdvertisementService().create(customer)


@router.get('/list', response_model=List[AdvertisementExpose])
async def get_customers(offset: int, limit: int):
    return await AdvertisementService().list(offset, limit)


@router.get('/advertisement/{location}',
            response_model=AdvertisementExpose)
async def get_by_location(member_id: int):
    return await AdvertisementService().get_by_location(member_id)


@router.get('/advertisement/{redis_channel_id}',
            response_model=AdvertisementExpose)
async def get_by_redis_channel_id(phone: int):
    return await AdvertisementService().get_by_redis_channel_id(phone)


@router.get('/advertisement/{publisher_id}', response_model=AdvertisementExpose)
async def get_by_publisher_id(nickname: str):
    return await AdvertisementService().get_by_publisher_id(nickname)


@router.put('/update', response_model=AdvertisementExpose)
async def create_customer(customer: CustomerUpdate):
    return await AdvertisementService().update(customer)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_member_id(member_id: int):
    await AdvertisementService().delete(member_id)
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