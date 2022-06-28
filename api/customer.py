from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

import schemas
from crud.customer import CustomerService
from db.models import Customer

router = APIRouter(
    prefix='/customer',
    tags=['Customer'],
)


@router.post('/create', response_model=schemas.Customer)
async def create_customer(customer: schemas.CustomerCreate):
    return await CustomerService().create(customer)


@router.get('/list', response_model=List[schemas.Customer])
async def get_customers(offset: int, limit: int):
    return await CustomerService().list(offset, limit)


@router.get('/member_id/{member_id}',
            response_model=schemas.Customer)
async def get_by_member_id(member_id: int):
    return await CustomerService().get_by_member_id(member_id)


@router.get('/phone/{phone}',
            response_model=schemas.Customer)
async def get_by_phone(phone: int):
    return await CustomerService().get_by_phone(phone)


@router.get('/nickname/{nickname}', response_model=schemas.Customer)
async def get_by_nickname(nickname: str):
    return await CustomerService().get_by_nickname(nickname)


@router.put('/update', response_model=schemas.Customer)
async def create_customer(customer: schemas.CustomerUpdate):
    return await CustomerService().update(customer)


@router.delete('/delete', response_model=schemas.Customer)
async def delete_by_member_id(member_id: int):
    return await CustomerService().delete(member_id)
