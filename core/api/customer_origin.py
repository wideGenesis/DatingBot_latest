from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from core import schemas
from core.crud.auth import get_current_user
from core.crud.customer import CustomerService


router = APIRouter(
    prefix='/customer',
    tags=['Customer'],
)


@router.get(
    '/',
    response_model=List[schemas.CustomerExpose],
)
def get_customers(
    user: schemas.User = Depends(get_current_user),
    customer_service: CustomerService = Depends(),
):
    return customer_service.get_many(user.id)


@router.post(
    '/',
    response_model=schemas.CustomerExpose,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_data: schemas.CustomerCreate,
    user: schemas.User = Depends(get_current_user),
    customer_service: CustomerService = Depends(),
):
    return customer_service.create(
        user.id,
        customer_data,
    )


@router.get(
    '/{customer_id}',
    response_model=schemas.CustomerExpose,
)
def get_customer(
    customer_id: int,
    user: schemas.User = Depends(get_current_user),
    customer_service: CustomerService = Depends(),
):
    return customer_service.get(
        user.id,
        customer_id,
    )


@router.put(
    '/{customer_id}',
    response_model=schemas.CustomerExpose,
)
def update_customer(
    customer_id: int,
    customer_data: schemas.CustomerUpdate,
    user: schemas.User = Depends(get_current_user),
    customer_service: CustomerService = Depends(),
):
    return customer_service.update(
        user.id,
        customer_id,
        customer_data,
    )


@router.delete(
    '/{customer_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
    customer_id: int,
    user: schemas.User = Depends(get_current_user),
    customer_service: CustomerService = Depends(),
):
    customer_service.delete(
        user.id,
        customer_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
