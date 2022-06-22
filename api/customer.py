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


# @router.get('/', response_model=List[schemas.Customer])
@router.get('/')
async def get_customers(limit: int):
    # return await Customer.objects.paginate(3).all()
    return await Customer.objects.all()


@router.get('/{customer_id}',
            response_model=Customer,
            response_model_exclude={
                'conversation_reference',
                'post_header',
                'passcode'}
            )
async def get_customer(customer_id: int):
    return await Customer.objects.get_or_none(id=customer_id)
