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

from core import schemas
from core.tables import models
from db.engine import get_session


class AdvertisementService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_id: int) -> List[models.Advertisement]:
        operations = (
            self.session
            .query(models.Advertisement)
            .filter(models.Advertisement.user_id == user_id)
            .order_by(
                models.Advertisement.date.desc(),
                models.Advertisement.id.desc(),
            )
            .all()
        )
        return operations

    def get(
        self,
        user_id: int,
        operation_id: int
    ) -> models.Advertisement:
        operation = self._get(user_id, operation_id)
        return operation

    def create_many(
        self,
        user_id: int,
        operations_data: List[schemas.AdvertisementCreate],
    ) -> List[models.Advertisement]:
        operations = [
            models.Advertisement(
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
        operation_data: schemas.AdvertisementCreate,
    ) -> models.Advertisement:
        operation = models.Advertisement(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(
        self,
        user_id: int,
        operation_id: int,
        operation_data: schemas.AdvertisementUpdate,
    ) -> models.Advertisement:
        operation = self._get(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(
        self,
        user_id: int,
        operation_id: int,
    ):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()

    def _get(self, user_id: int, operation_id: int) -> Optional[models.Advertisement]:
        operation = (
            self.session
            .query(models.Advertisement)
            .filter(
                models.Advertisement.user_id == user_id,
                models.Advertisement.id == operation_id,
            )
            .first()
        )
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return operation
