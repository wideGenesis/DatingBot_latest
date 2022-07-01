from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from core import schemas

# from crud.auth import get_current_user
from core.crud.customer import CustomerService


router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)


@router.get(
    "/",
    response_model=List[schemas.CustomerExpose],
)
def get_customers(
    customer: schemas.CustomerExpose,
    customer_service: CustomerService = Depends(),
):
    return customer_service.get_many(50)


@router.post(
    "/",
    response_model=schemas.CustomerExpose,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_data: schemas.CustomerCreate,
    customer: schemas.CustomerExpose,
    customer_service: CustomerService = Depends(),
):
    return customer_service.create(
        customer.id,
        customer_data,
    )


@router.get(
    "/{customer_id}",
    response_model=schemas.CustomerExpose,
)
def get_customer(
    customer_id: int,
    customer: schemas.CustomerExpose,
    customer_service: CustomerService = Depends(),
):
    return customer_service.get(
        customer.id,
    )


@router.put(
    "/{customer_id}",
    response_model=schemas.CustomerExpose,
)
def update_customer(
    customer_id: int,
    customer_data: schemas.CustomerUpdate,
    customer: schemas.CustomerExpose,
    customer_service: CustomerService = Depends(),
):
    return customer_service.update(
        customer.id,
        customer_id,
        customer_data,
    )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
    customer_id: int,
    customer: schemas.CustomerExpose,
    customer_service: CustomerService = Depends(),
):
    customer_service.delete(
        customer.id,
        customer_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
