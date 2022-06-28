
from fastapi import Depends, HTTPException, status

import schemas
from db import models


class CustomerService:

    async def create(self, customer: schemas.CustomerCreate) -> models.Customer:
        return await models.Customer(**customer.dict()).save()

    async def get_by_member_id(self, member_id: int) -> models.Customer:
        _customer = await models.Customer.objects.get_or_none(member_id=member_id)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def get_by_phone(self, phone: int) -> models.Customer:
        _customer = await models.Customer.objects.get_or_none(phone=phone)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

    async def get_by_nickname(self, nickname: str) -> models.Customer:
        _customer = await models.Customer.objects.get_or_none(nickname=nickname)
        if not _customer:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return _customer

        # async def update(self, user_data: CustomerProfile, column_names: list) -> models.Customer:
        #     customer = await Customer.objects.get(member_id=user_data.member_id)
        #     # customer.name = "Terminator 2"
        # # customer.year = 1991
        # # customer.profit = 0.520
        # # operation = await customer.update(_columns=column_names)
        # operation = await customer.update(**user_data.__dict__)

        # return operation

    async def update(self, customer: schemas.CustomerUpdate) -> models.Customer:
        return await models.Customer(**customer.dict()).save()

    async def delete(self, member_id: int) -> models.Customer.id:
        customer = await models.Customer.objects.get(member_id=member_id)
        deleted_id = await customer.delete()
        return deleted_id

    async def list(self, offset: int, limit: int) -> models.Customer:
        return await models.Customer.objects.offset(offset).limit(limit).all()

