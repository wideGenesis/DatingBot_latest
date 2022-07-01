# from typing import List
#
# from fastapi import (
#     APIRouter,
#     Response,
#     status,
# )
#
# from core.schemas.customer import CustomerExpose, CustomerCreate, CustomerUpdate
# from core.crud.customer import CustomerService
#
# router = APIRouter(
#     prefix='/customer',
#     tags=['Customer'],
# )
#
#
# @router.post('/create', response_model=CustomerExpose, status_code=status.HTTP_201_CREATED)
# async def create_customer(customer: CustomerCreate):
#     return await CustomerService().create(customer)
#
#
# @router.get('/list', response_model=List[CustomerExpose])
# async def get_customers(offset: int, limit: int):
#     return await CustomerService().list(offset, limit)
#
#
# @router.get('/list-by-city', response_model=List[CustomerExpose])
# async def list_by_city(offset: int, limit: int, city: str):
#     return await CustomerService().list_by_city(offset, limit, city)
#
#
# @router.get('/member_id/{member_id}',
#             response_model=CustomerExpose)
# async def get_by_member_id(member_id: int):
#     return await CustomerService().get_by_member_id(member_id)
#
#
# @router.get('/phone/{phone}',
#             response_model=CustomerExpose)
# async def get_by_phone(phone: int):
#     return await CustomerService().get_by_phone(phone)
#
#
# @router.get('/nickname/{nickname}', response_model=CustomerExpose)
# async def get_by_nickname(nickname: str):
#     return await CustomerService().get_by_nickname(nickname)
#
#
# @router.put('/update', response_model=CustomerExpose)
# async def update_customer(customer: CustomerUpdate):
#     return await CustomerService().update(customer)
#
#
# @router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_customer_by_member_id(member_id: int):
#     await CustomerService().delete(member_id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
