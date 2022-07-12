from typing import List

from fastapi import (
    APIRouter,
    Response,
    status,
    Depends,
)
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi.openapi.models import APIKey
from core.services.api_service import ApiKeyService
from core.tables.models import Customer, Area


from core.crud.customer import (
    CustomerService,
    EXCLUDE_FOR_LIST,
    EXCLUDE_FOR_LIST_BY_CITY,
    EXCLUDE_FOR_GET,
    EXCLUDE_FOR_POST,
)


router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)


@router.post(
    "/create/customer/",
    response_model=Customer,
    # response_model_exclude=EXCLUDE_FOR_POST,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    customer: Customer,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().create(customer)


@router.get(
    "/list/",
    response_model=List[Customer],
    # response_model_exclude=EXCLUDE_FOR_LIST,
    status_code=status.HTTP_201_CREATED,
)
async def list_customers(
        offset: int,
        limit: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await Customer.objects.offset(offset).limit(limit).all()


@router.get(
    "/list-by/{city}",
    response_model=List[Customer],
    # response_model_exclude=EXCLUDE_FOR_LIST_BY_CITY,
    status_code=status.HTTP_201_CREATED,
)
async def list_by_city(
    offset: int,
    limit: int,
    city_id: int,
    api_key: APIKey = Depends(ApiKeyService.get_api_key),
):
    return await CustomerService().list_by_city(offset, limit, city_id)


@router.get(
    "/get-by/{member-id}",
    response_model=Customer,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_member_id(
        member_id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().get_by_member_id(member_id)


@router.get(
    "/get-by-mobile/{phone}",
    response_model=Customer,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_phone(
        phone: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().get_by_phone(phone)


@router.get(
    "/get-by-nick/{nickname}",
    response_model=Customer,
    # response_model_exclude=EXCLUDE_FOR_GET,
    status_code=status.HTTP_201_CREATED,
)
async def get_by_nickname(
        nickname: str,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().get_by_nickname(nickname)


@router.put("/update/", response_model=Customer)
async def update_customer(
        customer: Customer,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().update(customer)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(
        _id: int,
        api_key: APIKey = Depends(ApiKeyService.get_api_key)
):
    return await CustomerService().delete(_id)
