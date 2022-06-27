from typing import  List, Optional
from fastapi import Depends, HTTPException, status


import schemas
from db import models
from db.models import Customer
from ms_bot.bots_models import CustomerProfile


class CustomerService:

    async def get_many(self, _limit: int) -> List[Customer]:
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

    async def create(self, user_data: CustomerProfile, operation_data: schemas.CustomerCreate) -> models.Customer:
        operation = await Customer(
            nickname=user_data.nickname,
            phone=int(user_data.phone),
            premium_tier_id=1,
            conversation_reference=user_data.conversation_reference,
            member_id=int(user_data.member_id),
            lang=int(user_data.lang),
            is_active=int(user_data.is_active)
        ).save()
        return operation

    async def read(self, member_id: int) -> models.Customer:
        operation = await Customer.objects.get_or_none(member_id=member_id)
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return operation

    async def update(self, member_id: int, column_names: list, operation_data: schemas.CustomerUpdate) -> models.Customer:
        customer = await Customer.objects.get(member_id=member_id)
        customer.name = "Terminator 2"
        customer.year = 1991
        customer.profit = 0.520
        operation = await customer.update(_columns=column_names)

        return operation

    # def create(self, user_id: int, operation_data: schemas.CustomerCreate) -> models.Customer:
    #     operation = models.Customer( **operation_data.dict(), user_id=user_id)
    #     self.session.add(operation)
    #     self.session.commit()
    #     return operation

    async def delete(self, member_id: int) -> models.Customer.id:
        customer = await Customer.objects.get(name='The Bird')
        deleted_id = await customer.delete()
        return deleted_id

    async def list(self, member_id: int, phone: int) -> models.Customer:
        operation = None
        if member_id:
                operation = await Customer.objects.filter(customer__member_id=member_id).all()
        if phone:
                operation = await Customer.objects.filter(customer__phone=phone).all()
        return operation
