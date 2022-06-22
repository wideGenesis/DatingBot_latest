from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

import schemas
from db import models
from db.engine import get_session
from db.models import Customer


class CustomerService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_many(self, _limit: int) -> List[Customer]:
        return await Customer.objects.get().all()

    async def get_by_id(self, customer_id: int) -> Customer:
        return await Customer.objects.get_or_none(id=customer_id).first()

    async def get_by_member_id(self, member_id: int) -> Customer:
        return await Customer.objects.get_or_none(member_id=member_id).first()

    def create_many(
        self,
        user_id: int,
        operations_data: List[schemas.CustomerCreate],
    ) -> List[models.Customer]:
        operations = [
            models.Customer(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        return operations

    def create(
        self,
        user_id: int,
        operation_data: schemas.CustomerCreate,
    ) -> models.Customer:
        operation = models.Customer(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(
        self,
        user_id: int,
        operation_data: schemas.CustomerUpdate,
    ) -> models.Customer:
        operation = self._get(user_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(
        self,
        user_id: int,
    ):
        operation = self._get(user_id)
        self.session.delete(operation)
        self.session.commit()

    def _get(self, user_id: int) -> Optional[models.Customer]:
        operation = (
            self.session
            .query(models.Customer)
            .filter(
                models.Customer.user_id == user_id,
            )
            .first()
        )
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return operation
