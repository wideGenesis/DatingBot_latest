from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from core.crud.customer import CustomerService, EXCLUDE_FOR_LIST, EXCLUDE_FOR_LIST_BY_CITY, EXCLUDE_FOR_MEMBER_ID
from core.tables.models import Customer, Area, RedisChannel

router = APIRouter(
    prefix='/customer',
    tags=['Customer'],
)


@router.post('/create', response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: Customer):
    return await Customer(**customer.dict()).create(customer)


@router.get('/list',
            response_model=List[Customer],
            response_model_exclude=EXCLUDE_FOR_LIST,
            status_code=status.HTTP_201_CREATED
            )
async def list_customers(offset: int, limit: int):
    return await Customer.objects.offset(offset).limit(limit).select_related(
        'premium_tier_id').select_related(
        'redis_channel_id').all()


@router.get('/list-by-city/{city}',
            response_model=List[Customer],
            response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
            status_code=status.HTTP_201_CREATED
            )
async def list_by_city(offset: int, limit: int, city: str):
    city_obj = await Area.objects.get_or_none(city=city.lower())
    if city_obj is None:
        city_obj = await Area.objects.get_or_none(city_en=city.lower())
        if city_obj is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    city_id = city_obj.__dict__
    city_id = city_id['id']
    return await Customer.objects.offset(offset).limit(limit).filter(
        city=city_id).all()


@router.get('/list-by-redis_channel/{channel}',
            response_model=List[Customer],
            response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
            status_code=status.HTTP_201_CREATED
            )
async def list_by_redis_channel(offset: int, limit: int, redis_channel: str):
    channel_obj = await RedisChannel.objects.get_or_none(redis_channel=redis_channel.lower())
    if channel_obj is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    channel_id = channel_obj.__dict__
    channel_id = channel_id['id']
    return await Customer.objects.offset(offset).limit(limit).filter(
        redis_channel_id=channel_id).all()


@router.get('/{member_id}',
            response_model=Customer,
            response_model_exclude=EXCLUDE_FOR_MEMBER_ID,
            status_code=status.HTTP_201_CREATED
            )
async def get_by_member_id(member_id: int):
    customer = await Customer.objects.get_or_none(member_id=member_id)
    return customer


@router.get('/{phone}',
            response_model=Customer)
async def get_by_phone(phone: int):
    return await CustomerService().get_by_phone(phone)


@router.get('/{nickname}', response_model=Customer)
async def get_by_nickname(nickname: str):
    return await CustomerService().get_by_nickname(nickname)


@router.put('/update', response_model=Customer)
async def update_customer(customer: Customer):
    return await CustomerService().update(customer)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_member_id(member_id: int):
    await CustomerService().delete(member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
