from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
)

from core.crud.customer import CustomerService, EXCLUDE
from core.tables.models import Customer, Area

router = APIRouter(
    prefix='/customer',
    tags=['Customer'],
)


@router.post('/create/1', response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: Customer):
    return await Customer(**customer.dict()).create(customer)


@router.get('/list/1',
            response_model=List[Customer],
            response_model_exclude=EXCLUDE,
            status_code=status.HTTP_201_CREATED
            )
async def get_customers(offset: int, limit: int):
    return await Customer.objects.offset(offset).limit(limit).select_related(
        'premium_tier_id').select_related(
        'redis_channel_id').all()


@router.get('/list-by-city/{city}', response_model=List[Customer])
async def list_by_city(offset: int, limit: int, city: str):
    city_id = await Area.objects.filter(city=city).first()
    print('city_list', type(city_id))
    print('city_list', dir(city_id))
    return await Customer.objects.offset(offset).limit(limit).filter(city=city_id).all()


@router.get('/member_id/{member_id}/1',
            response_model=Customer)
async def get_by_member_id(member_id: int):
    return await CustomerService().get_by_member_id(member_id)


@router.get('/phone/{phone}/1',
            response_model=Customer)
async def get_by_phone(phone: int):
    return await CustomerService().get_by_phone(phone)


@router.get('/nickname/{nickname}/1', response_model=Customer)
async def get_by_nickname(nickname: str):
    return await CustomerService().get_by_nickname(nickname)


@router.put('/update/1', response_model=Customer)
async def update_customer(customer: Customer):
    return await CustomerService().update(customer)


@router.delete('/delete/1', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_member_id(member_id: int):
    await CustomerService().delete(member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
